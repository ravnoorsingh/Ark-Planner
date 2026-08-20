"""The `data/` document store.

Paths are a pure function of (library, role, rank, url), so re-scraping a page
overwrites it in place — "latest docs" stays latest, and a future RAG index gets
stable identifiers. Freshness lives in the manifest and each file's front matter,
never in the path.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from .state import Manifest, ScrapedDoc
from .tracing import annotate, traced

MANIFEST_NAME = "manifest.json"
_SLUG_STRIP = re.compile(r"[^a-z0-9]+")
_MAX_SLUG = 80


def _slugify(text: str, limit: int) -> str:
    return _SLUG_STRIP.sub("-", text.lower()).strip("-")[:limit].strip("-")


def url_slug(url: str) -> str:
    """Filesystem-safe slug for a URL: host + path, disambiguated by a hash.

    The hash suffix matters — truncation and character folding both collapse
    distinct URLs (long doc paths, `?version=` query strings), and a collision
    would silently overwrite one page's content with another's.
    """
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.netloc.lower().removeprefix("www.")
    tail = parsed.path
    if parsed.query:
        tail = f"{tail}-{parsed.query}"

    slug = _slugify(f"{host}{tail}", _MAX_SLUG) or "page"
    digest = hashlib.sha256(url.strip().encode()).hexdigest()[:8]
    return f"{slug}-{digest}"


def portable(path: Path) -> str:
    """Record paths relative to the working directory when possible.

    An absolute path would pin the manifest to one machine; the store is meant to
    be committable and readable by later pipeline phases wherever it is checked out.
    """
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


QUERY_SLUG_LIMIT = 48


def library_dir(data_dir: Path, library: str, query: str = "") -> Path:
    """`data/<library>-<query>/` so a run's docs stay together and legible.

    Parentheses are deliberately left out of the name: they are legal on disk but
    force quoting in every shell glob over the store.
    """
    name = _slugify(library, 60) or "unknown"
    slug = _slugify(query, QUERY_SLUG_LIMIT)
    return data_dir / (f"{name}-{slug}" if slug else name)


def doc_paths(
    data_dir: Path, library: str, role: str, rank: int, url: str, query: str = ""
) -> tuple[Path, Path]:
    """Return the (markdown, raw JSON) paths for one document."""
    prefix = "primary" if role == "primary" else f"alt-{rank}"
    stem = f"{prefix}--{url_slug(url)}"
    directory = library_dir(data_dir, library, query)
    return directory / f"{stem}.md", directory / f"{stem}.json"


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def front_matter(fields: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if value is None or value == "":
            continue
        rendered = f'"{_escape(value)}"' if isinstance(value, str) else value
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


@traced("write_document", run_type="tool")
def write_document(
    data_dir: Path,
    *,
    library: str,
    url: str,
    role: str,
    rank: int,
    markdown: str,
    raw_row: dict | None,
    title: str = "",
    fetched_via: str = "",
    resolved_url: str = "",
    query: str = "",
    from_cache: bool = False,
) -> ScrapedDoc:
    """Write one page's markdown (with front matter) and its raw row sidecar."""
    md_path, raw_path = doc_paths(data_dir, library, role, rank, url, query)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    fetched_at = datetime.now(UTC).isoformat()
    body = markdown.strip()
    digest = hashlib.sha256(body.encode()).hexdigest()

    header = front_matter(
        {
            "library": library,
            "query": query,
            "url": url,
            # Only present when the content came from somewhere else — anything
            # citing this file must point at where the text actually lives.
            "resolved_url": resolved_url,
            "role": role,
            "rank": rank,
            "title": title,
            "fetched_at": fetched_at,
            # How this page was fetched — provenance for anything citing it.
            "fetched_via": fetched_via,
            "sha256": digest,
        }
    )
    md_path.write_text(f"{header}\n\n{body}\n", encoding="utf-8")

    if raw_row is not None:
        raw_path.write_text(json.dumps(raw_row, indent=2, ensure_ascii=False), encoding="utf-8")

    annotate(
        path=portable(md_path),
        markdown_bytes=len(body.encode()),
        sha256=digest,
        redirected=bool(resolved_url),
    )
    return ScrapedDoc(
        library=library,
        query=query,
        url=url,
        resolved_url=resolved_url,
        role=role,  # type: ignore[arg-type]
        rank=rank,
        status="ok" if body else "empty",
        path=portable(md_path),
        raw_path=portable(raw_path) if raw_row is not None else None,
        title=title,
        bytes=len(body.encode()),
        sha256=digest,
        fetched_at=fetched_at,
        from_cache=from_cache,
        error=None if body else "Collector returned no usable page content",
    )


def failed_document(
    library: str, url: str, role: str, rank: int, error: str, query: str = ""
) -> ScrapedDoc:
    """A URL the collector never returned — recorded, never silently dropped."""
    return ScrapedDoc(
        library=library,
        query=query,
        url=url,
        role=role,  # type: ignore[arg-type]
        rank=rank,
        status="failed",
        fetched_at=datetime.now(UTC).isoformat(),
        error=error,
    )


@traced("load_manifest", run_type="tool")
def load_manifest(data_dir: Path) -> Manifest:
    path = data_dir / MANIFEST_NAME
    if not path.exists():
        return Manifest()
    try:
        return Manifest.model_validate_json(path.read_text(encoding="utf-8"))
    except ValueError:
        # A corrupt manifest must not block a scrape; the files are the source of
        # truth and the manifest is rebuilt from what we just wrote.
        return Manifest()


@traced("merge_manifest", run_type="tool")
def merge_manifest(
    manifest: Manifest, documents: list[ScrapedDoc], fetched_via: str = ""
) -> Manifest:
    """Upsert documents on (library, url) so re-scrapes update instead of duplicating."""
    index = {doc.key: doc for doc in manifest.documents}
    for doc in documents:
        index[doc.key] = doc
    return Manifest(
        updated_at=datetime.now(UTC).isoformat(),
        fetched_via=fetched_via or manifest.fetched_via,
        documents=sorted(index.values(), key=lambda doc: (doc.library, doc.rank, doc.url)),
    )


@traced("save_manifest", run_type="tool")
def save_manifest(data_dir: Path, manifest: Manifest) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / MANIFEST_NAME
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return path
