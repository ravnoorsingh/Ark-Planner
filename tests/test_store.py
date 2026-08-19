"""The data/ store: slugging, paths, front matter, and manifest merging."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ark.state import Manifest
from ark.store import (
    doc_paths,
    failed_document,
    front_matter,
    load_manifest,
    merge_manifest,
    save_manifest,
    url_slug,
    write_document,
)

# --- slugging ----------------------------------------------------------------------


def test_slug_is_filesystem_safe():
    slug = url_slug("https://docs.langchain.com/oss/python/langgraph/overview")
    assert slug.replace("-", "").isalnum()
    assert "/" not in slug and ":" not in slug


def test_slug_drops_www_and_scheme():
    assert url_slug("https://www.python-httpx.org").startswith("python-httpx-org")


def test_slug_is_stable_for_the_same_url():
    assert url_slug("https://fastapi.tiangolo.com") == url_slug("https://fastapi.tiangolo.com")


@pytest.mark.parametrize(
    ("a", "b"),
    [
        # Differ only past the length cap.
        ("https://x.dev/" + "a" * 100 + "/one", "https://x.dev/" + "a" * 100 + "/two"),
        # Differ only in the query string.
        ("https://x.dev/docs?version=1", "https://x.dev/docs?version=2"),
        # Differ only by characters the slugifier folds away.
        ("https://x.dev/a_b", "https://x.dev/a.b"),
        ("https://x.dev/a/b", "https://x.dev/a-b"),
    ],
)
def test_distinct_urls_never_collide(a, b):
    """A collision would silently overwrite one page's content with another's."""
    assert url_slug(a) != url_slug(b)


def test_slug_handles_unicode_paths():
    slug = url_slug("https://x.dev/docs/日本語/ガイド")
    assert slug and slug.replace("-", "").isalnum()


def test_slug_length_is_bounded():
    assert len(url_slug("https://x.dev/" + "segment/" * 100)) <= 100


def test_slug_survives_a_bare_host():
    assert url_slug("fastapi.tiangolo.com").startswith("fastapi-tiangolo-com")


# --- paths -------------------------------------------------------------------------


def test_primary_and_alternate_paths_are_distinguishable(tmp_path):
    md, raw = doc_paths(tmp_path, "fastapi", "primary", 0, "https://fastapi.tiangolo.com")
    assert md.parent.name == "fastapi"
    assert md.name.startswith("primary--")
    assert raw.suffix == ".json"
    assert md.stem == raw.stem

    alt, _ = doc_paths(tmp_path, "fastapi", "alternate", 2, "https://github.com/fastapi/fastapi")
    assert alt.name.startswith("alt-2--")


def test_library_names_are_slugged_into_safe_directories(tmp_path):
    md, _ = doc_paths(tmp_path, "@scope/Some Pkg", "primary", 0, "https://x.dev")
    assert "/" not in md.parent.name
    assert md.parent.name == "scope-some-pkg"


def test_paths_are_a_pure_function_of_their_inputs(tmp_path):
    """Stability is what makes a re-scrape overwrite instead of accumulating."""
    args = (tmp_path, "fastapi", "primary", 0, "https://fastapi.tiangolo.com")
    assert doc_paths(*args) == doc_paths(*args)


# --- front matter ------------------------------------------------------------------


def test_front_matter_quotes_and_skips_empties():
    text = front_matter({"library": "fastapi", "rank": 0, "title": "", "note": None})
    assert text.startswith("---") and text.endswith("---")
    assert 'library: "fastapi"' in text
    assert "rank: 0" in text
    assert "title:" not in text and "note:" not in text


def test_front_matter_escapes_quotes_and_newlines():
    text = front_matter({"title": 'He said "hi"\nthen left'})
    assert '\\"hi\\"' in text
    assert text.count("\n") == 2  # only the delimiters, no injected line break


# --- writing -----------------------------------------------------------------------


def test_write_document_produces_markdown_and_sidecar(tmp_path):
    doc = write_document(
        tmp_path,
        library="fastapi",
        url="https://fastapi.tiangolo.com",
        role="primary",
        rank=0,
        markdown="# FastAPI\n\nA web framework.",
        raw_row={"url": "https://fastapi.tiangolo.com", "markdown": "# FastAPI"},
        title="FastAPI",
        fetched_via="brightdata-unlocker:cli_unlocker",
    )

    assert doc.status == "ok"
    text = Path(doc.path).read_text(encoding="utf-8")
    assert 'library: "fastapi"' in text
    assert 'fetched_via: "brightdata-unlocker:cli_unlocker"' in text
    assert "# FastAPI" in text
    assert doc.bytes > 0 and len(doc.sha256) == 64

    raw = json.loads(Path(doc.raw_path).read_text(encoding="utf-8"))
    assert raw["url"] == "https://fastapi.tiangolo.com"


def test_empty_content_is_flagged_not_silently_stored(tmp_path):
    doc = write_document(
        tmp_path,
        library="x",
        url="https://x.dev",
        role="primary",
        rank=0,
        markdown="   ",
        raw_row={"url": "https://x.dev"},
    )
    assert doc.status == "empty"
    assert doc.error and "no usable page content" in doc.error


def test_rescrape_overwrites_in_place(tmp_path):
    def write(markdown: str):
        return write_document(
            tmp_path,
            library="fastapi",
            url="https://fastapi.tiangolo.com",
            role="primary",
            rank=0,
            markdown=markdown,
            raw_row={"markdown": markdown},
        )

    first = write("# Old content")
    second = write("# New content")

    assert first.path == second.path
    assert first.sha256 != second.sha256
    assert "# New content" in Path(second.path).read_text(encoding="utf-8")
    assert len(list((tmp_path / "fastapi").glob("*.md"))) == 1


def test_failed_document_records_the_attempt(tmp_path):
    doc = failed_document("x", "https://x.dev", "alternate", 1, "no row returned")
    assert doc.status == "failed"
    assert doc.path is None and doc.raw_path is None
    assert doc.error == "no row returned"


# --- manifest ----------------------------------------------------------------------


def _doc(tmp_path, library: str, url: str, markdown: str = "# hi"):
    return write_document(
        tmp_path, library=library, url=url, role="primary", rank=0,
        markdown=markdown, raw_row={"markdown": markdown},
    )


def test_missing_manifest_loads_as_empty(tmp_path):
    assert load_manifest(tmp_path).documents == []


def test_corrupt_manifest_does_not_block_a_scrape(tmp_path):
    (tmp_path / "manifest.json").write_text("{ not json", encoding="utf-8")
    assert load_manifest(tmp_path).documents == []


def test_manifest_round_trips(tmp_path):
    docs = [_doc(tmp_path, "fastapi", "https://fastapi.tiangolo.com")]
    save_manifest(tmp_path, merge_manifest(Manifest(), docs, "c_1"))

    loaded = load_manifest(tmp_path)
    assert loaded.fetched_via == "c_1"
    assert [d.url for d in loaded.documents] == ["https://fastapi.tiangolo.com"]


def test_rescrape_upserts_rather_than_duplicating(tmp_path):
    url = "https://fastapi.tiangolo.com"
    manifest = merge_manifest(Manifest(), [_doc(tmp_path, "fastapi", url, "# v1")])
    manifest = merge_manifest(manifest, [_doc(tmp_path, "fastapi", url, "# v2 longer")])

    assert len(manifest.documents) == 1
    assert manifest.documents[0].bytes == len("# v2 longer")


def test_same_url_under_two_libraries_is_two_entries(tmp_path):
    url = "https://docs.langchain.com"
    manifest = merge_manifest(Manifest(), [_doc(tmp_path, "langchain", url)])
    manifest = merge_manifest(manifest, [_doc(tmp_path, "langgraph", url)])
    assert len(manifest.documents) == 2


def test_merge_preserves_prior_provenance_when_not_supplied(tmp_path):
    manifest = merge_manifest(Manifest(), [_doc(tmp_path, "a", "https://a.dev")], "c_first")
    manifest = merge_manifest(manifest, [_doc(tmp_path, "b", "https://b.dev")])
    assert manifest.fetched_via == "c_first"


def test_documents_are_sorted_for_stable_diffs(tmp_path):
    docs = [_doc(tmp_path, "zlib", "https://z.dev"), _doc(tmp_path, "alib", "https://a.dev")]
    manifest = merge_manifest(Manifest(), docs)
    assert [d.library for d in manifest.documents] == ["alib", "zlib"]


# --- query-scoped folders -------------------------------------------------------------


def test_folder_carries_the_query(tmp_path):
    md, _ = doc_paths(tmp_path, "fastapi", "primary", 0, "https://x.dev",
                      "build a REST API with FastAPI")
    assert md.parent.name == "fastapi-build-a-rest-api-with-fastapi"


def test_folder_is_just_the_library_when_no_query(tmp_path):
    md, _ = doc_paths(tmp_path, "fastapi", "primary", 0, "https://x.dev")
    assert md.parent.name == "fastapi"


def test_long_queries_are_truncated(tmp_path):
    md, _ = doc_paths(tmp_path, "x", "primary", 0, "https://x.dev", "word " * 100)
    assert len(md.parent.name) < 80


def test_query_slug_is_shell_safe(tmp_path):
    """No parentheses or spaces: the store gets globbed constantly."""
    md, _ = doc_paths(tmp_path, "x", "primary", 0, "https://x.dev", "a (weird) query!")
    assert set(md.parent.name) <= set("abcdefghijklmnopqrstuvwxyz0123456789-")


def test_same_library_two_queries_lands_in_two_folders(tmp_path):
    a, _ = doc_paths(tmp_path, "fastapi", "primary", 0, "https://x.dev", "build an API")
    b, _ = doc_paths(tmp_path, "fastapi", "primary", 0, "https://x.dev", "build a CLI")
    assert a != b


def test_manifest_keeps_both_queries_separate(tmp_path):
    def doc(query):
        return write_document(
            tmp_path, library="fastapi", url="https://x.dev", role="primary", rank=0,
            markdown="# hi", raw_row={}, query=query,
        )

    manifest = merge_manifest(Manifest(), [doc("build an API")])
    manifest = merge_manifest(manifest, [doc("build a CLI")])
    # Collapsing these would leave one entry pointing at the other run's file.
    assert len(manifest.documents) == 2


def test_rescrape_of_the_same_query_still_upserts(tmp_path):
    def doc():
        return write_document(
            tmp_path, library="fastapi", url="https://x.dev", role="primary", rank=0,
            markdown="# hi", raw_row={}, query="build an API",
        )

    manifest = merge_manifest(Manifest(), [doc()])
    manifest = merge_manifest(manifest, [doc()])
    assert len(manifest.documents) == 1


def test_query_is_recorded_in_front_matter(tmp_path):
    doc = write_document(
        tmp_path, library="fastapi", url="https://x.dev", role="primary", rank=0,
        markdown="# hi", raw_row={}, query="build a REST API",
    )
    assert 'query: "build a REST API"' in Path(doc.path).read_text()
