"""MongoDB store: a system of record for runs and plans, and a scrape cache.

The filesystem stays the artifact — a plan's citations point at local files with a
sha256, and that should remain one `cat` away rather than needing a database client.
Mongo is additive:

* `runs` and `plans` make history queryable instead of greppable.
* `documents` is keyed by **URL**, not by query, which is what lets a later run reuse
  a page an earlier one paid to scrape.

Every write here is best-effort. Losing the database must never lose the run, so
failures surface as warnings and the filesystem output is produced regardless. With
no `MONGODB_URI` configured nothing in this module runs at all.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from pymongo import AsyncMongoClient, ReturnDocument
from pymongo.errors import PyMongoError

from .brightdata import normalize_url
from .config import Settings
from .tracing import annotate, traced

RUNS = "runs"
PLANS = "plans"
DOCUMENTS = "documents"
# The public side: what the catalogue lists, and one row per download so
# "trending" can mean "downloaded lately" rather than "downloaded ever".
CATALOG = "catalog"
INSTALLS = "installs"


def _midnight(moment: datetime) -> datetime:
    return moment.replace(hour=0, minute=0, second=0, microsecond=0)


class MongoStore:
    """Thin wrapper over the three collections. Construct with `connect()`."""

    def __init__(self, client: AsyncMongoClient, database: str) -> None:
        self._client = client
        self.db = client[database]

    # --- lifecycle ----------------------------------------------------------------

    async def ensure_indexes(self) -> None:
        await self.db[DOCUMENTS].create_index("fetched_at")
        await self.db[RUNS].create_index("generated_at")
        await self.db[PLANS].create_index([("run_id", 1), ("revision", 1)])
        await self.db[CATALOG].create_index("installs")
        await self.db[CATALOG].create_index("published_at")
        await self.db[CATALOG].create_index("libraries")
        # Free-text search over the parts a person actually types: the name first,
        # then what it is for, then the stack.
        await self.db[CATALOG].create_index(
            [("name", "text"), ("requirement", "text"), ("libraries", "text")],
            weights={"name": 10, "libraries": 4, "requirement": 1},
            name="catalog_search",
        )
        await self.db[INSTALLS].create_index([("slug", 1), ("at", -1)])

    async def close(self) -> None:
        await self._client.close()

    # --- the cache ----------------------------------------------------------------

    @staticmethod
    def key(url: str) -> str:
        """Cache key. Reuses the URL normalization the row matcher already relies on,
        so `https://x.dev` and `https://x.dev/` are one entry rather than two."""
        return normalize_url(url)

    @traced("cache_lookup", run_type="retriever")
    async def cached(self, urls: list[str], ttl_days: int) -> dict[str, dict]:
        """Return {url: document} for pages cached and still fresh.

        Anything older than the TTL is treated as a miss: the premise of this project
        is that documentation goes stale, so serving an old copy indefinitely would
        undermine the thing it exists to guarantee.
        """
        if not urls:
            return {}
        cutoff = datetime.now(UTC) - timedelta(days=ttl_days)
        keys = {self.key(url): url for url in urls}
        found: dict[str, dict] = {}
        try:
            cursor = self.db[DOCUMENTS].find({"_id": {"$in": list(keys)}})
            async for doc in cursor:
                fetched = doc.get("fetched_at")
                if fetched and fetched.replace(tzinfo=fetched.tzinfo or UTC) >= cutoff:
                    found[keys[doc["_id"]]] = doc
        except PyMongoError as exc:  # a cold cache is not a failure
            annotate(cache_error=str(exc)[:200])
            return {}
        annotate(requested=len(urls), hits=len(found))
        return found

    @traced("cache_store", run_type="tool")
    async def remember(self, url: str, payload: dict, query: str) -> None:
        """Store a successfully scraped page, recording which query used it."""
        try:
            await self.db[DOCUMENTS].update_one(
                {"_id": self.key(url)},
                {
                    "$set": {**payload, "url": url},
                    # Provenance, not identity: the same content serves any query.
                    "$addToSet": {"queries": query} if query else {},
                },
                upsert=True,
            )
        except PyMongoError as exc:
            annotate(cache_write_error=str(exc)[:200])

    async def reused(self, url: str, query: str) -> None:
        """Record that `query` was served this page from the cache.

        Deliberately does not touch `fetched_at`: a cache hit is not a refetch, and
        bumping the timestamp would keep a popular page alive past its TTL forever —
        the staleness the cache is meant to bound. Without this the `queries` array
        only ever names the run that first fetched a page, so every "pages the cache
        is serving most often" query reports one use each.
        """
        if not query:
            return
        try:
            await self.db[DOCUMENTS].update_one(
                {"_id": self.key(url)}, {"$addToSet": {"queries": query}}
            )
        except PyMongoError as exc:
            annotate(cache_touch_error=str(exc)[:200])

    # --- system of record ---------------------------------------------------------

    @traced("save_run", run_type="tool")
    async def save_run(self, run_id: str, payload: dict[str, Any]) -> None:
        try:
            await self.db[RUNS].update_one(
                {"_id": run_id}, {"$set": {**payload, "run_id": run_id}}, upsert=True
            )
        except PyMongoError as exc:
            annotate(run_write_error=str(exc)[:200])

    @traced("save_plan_revision", run_type="tool")
    async def save_plan(
        self, run_id: str, markdown: str, model: str, instruction: str | None = None
    ) -> int:
        """Append a revision rather than overwriting, so refinements stay inspectable."""
        try:
            latest = await self.db[PLANS].find_one(
                {"run_id": run_id}, sort=[("revision", -1)], projection={"revision": 1}
            )
            revision = (latest or {}).get("revision", 0) + 1
            await self.db[PLANS].insert_one(
                {
                    "run_id": run_id,
                    "revision": revision,
                    "instruction": instruction,
                    "markdown": markdown,
                    "model": model,
                    "created_at": datetime.now(UTC),
                }
            )
            return revision
        except PyMongoError as exc:
            annotate(plan_write_error=str(exc)[:200])
            return 0

    # --- the public catalogue ------------------------------------------------------

    @traced("publish_plan", run_type="tool")
    async def publish(self, slug: str, payload: dict[str, Any]) -> str:
        """List a plan publicly under `slug`, or update the listing if it exists.

        `installs` is set only on insert. Re-publishing a revised plan must not reset
        the download count — the count belongs to the entry, not to the revision.
        """
        try:
            await self.db[CATALOG].update_one(
                {"_id": slug},
                {
                    "$set": {**payload, "slug": slug, "updated_at": datetime.now(UTC)},
                    "$setOnInsert": {"installs": 0, "published_at": datetime.now(UTC)},
                },
                upsert=True,
            )
        except PyMongoError as exc:
            annotate(publish_error=str(exc)[:200])
            return ""
        return slug

    async def get_plan(self, slug: str) -> dict[str, Any] | None:
        try:
            return await self.db[CATALOG].find_one({"_id": slug})
        except PyMongoError:
            return None

    @traced("record_install", run_type="tool")
    async def record_install(self, slug: str) -> int:
        """Count a download, and log it so trending can be windowed by time.

        The counter and the event log are kept separately on purpose: the counter is
        what every listing reads, and recomputing it from millions of events on each
        page load would be the obvious way to make this slow.
        """
        try:
            updated = await self.db[CATALOG].find_one_and_update(
                {"_id": slug}, {"$inc": {"installs": 1}}, projection={"installs": 1},
                return_document=ReturnDocument.AFTER,
            )
            if updated is None:
                return 0
            await self.db[INSTALLS].insert_one({"slug": slug, "at": datetime.now(UTC)})
            return int(updated.get("installs", 0))
        except PyMongoError as exc:
            annotate(install_error=str(exc)[:200])
            return 0

    async def recent_installs(self, slugs: list[str], days: int = 7) -> dict[str, list[int]]:
        """Per-day download counts for each slug, oldest first, zero-filled.

        Zero-filling matters: a sparkline drawn only from days that had downloads
        would show a flat line for a plan downloaded twice a week apart.
        """
        if not slugs:
            return {}
        since = _midnight(datetime.now(UTC)) - timedelta(days=days - 1)
        buckets: dict[str, list[int]] = {slug: [0] * days for slug in slugs}
        try:
            cursor = await self.db[INSTALLS].aggregate(
                [
                    {"$match": {"slug": {"$in": slugs}, "at": {"$gte": since}}},
                    {
                        "$group": {
                            "_id": {
                                "slug": "$slug",
                                "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$at"}},
                            },
                            "n": {"$sum": 1},
                        }
                    },
                ]
            )
            async for row in cursor:
                slug = row["_id"]["slug"]
                day = datetime.strptime(row["_id"]["day"], "%Y-%m-%d").replace(tzinfo=UTC)
                index = (day - since).days
                if slug in buckets and 0 <= index < days:
                    buckets[slug][index] = row["n"]
        except PyMongoError as exc:
            annotate(trend_error=str(exc)[:200])
        return buckets

    @traced("search_catalog", run_type="retriever")
    async def search(
        self,
        query: str = "",
        *,
        sort: str = "installs",
        library: str = "",
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List catalogue entries, optionally filtered by text or by library.

        `trending` ranks by downloads in the last week rather than all time, so a
        plan published today can reach the top; `installs` and `new` are the stable
        orderings underneath it.
        """
        selector: dict[str, Any] = {}
        if library:
            selector["libraries"] = library
        projection = {"markdown": 0}
        try:
            if query:
                selector["$text"] = {"$search": query}
                projection["score"] = {"$meta": "textScore"}
                order: Any = [("score", {"$meta": "textScore"}), ("installs", -1)]
            elif sort == "new":
                order = [("published_at", -1)]
            else:
                order = [("installs", -1), ("published_at", -1)]
            cursor = self.db[CATALOG].find(selector, projection).sort(order).limit(limit)
            found = [row async for row in cursor]
        except PyMongoError as exc:
            annotate(search_error=str(exc)[:200])
            return []

        if sort == "trending" and not query:
            weekly = await self.recent_installs([row["_id"] for row in found])
            for row in found:
                row["recent"] = sum(weekly.get(row["_id"], []))
            # Ties on a fresh catalogue are common (everything at zero recent), so
            # fall back to all-time rather than leaving the order arbitrary.
            found.sort(key=lambda row: (row.get("recent", 0), row.get("installs", 0)), reverse=True)
        return found

    async def libraries(self, limit: int = 24) -> list[dict[str, Any]]:
        """The most-used libraries across the catalogue, for the topic filters."""
        try:
            cursor = await self.db[CATALOG].aggregate(
                [
                    {"$unwind": "$libraries"},
                    {"$group": {"_id": "$libraries", "n": {"$sum": 1}}},
                    {"$sort": {"n": -1}},
                    {"$limit": limit},
                ]
            )
            return [{"name": row["_id"], "plans": row["n"]} async for row in cursor]
        except PyMongoError:
            return []

    async def stats(self) -> dict[str, int]:
        return {
            "runs": await self.db[RUNS].count_documents({}),
            "plans": await self.db[PLANS].count_documents({}),
            "documents": await self.db[DOCUMENTS].count_documents({}),
            "catalog": await self.db[CATALOG].count_documents({}),
            "installs": await self.db[INSTALLS].count_documents({}),
        }


async def connect(settings: Settings) -> MongoStore | None:
    """Open a store, or return None when Mongo is not configured or not reachable.

    Returning None rather than raising is the point: the pipeline runs identically
    without a database, so an unreachable one degrades to the filesystem-only path.
    """
    if not settings.mongodb_uri:
        return None
    try:
        client: AsyncMongoClient = AsyncMongoClient(
            settings.mongodb_uri, serverSelectionTimeoutMS=settings.mongodb_timeout_ms
        )
        await client.admin.command("ping")
        store = MongoStore(client, settings.mongodb_db)
        await store.ensure_indexes()
        return store
    except PyMongoError:
        return None
