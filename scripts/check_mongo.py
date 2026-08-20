"""Verify the MongoDB connection, create indexes, and report what is stored.

    uv run python scripts/check_mongo.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

from ark.config import load_settings
from ark.mongo import connect


async def main() -> int:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    settings = load_settings()

    if not settings.mongodb_uri:
        print("MONGODB_URI is not set — ARK is running filesystem-only.")
        print("See docs/mongodb.md to enable the store and the scrape cache.")
        return 1

    # Hide any password in the URI before printing it.
    shown = settings.mongodb_uri
    if "@" in shown:
        scheme, _, rest = shown.partition("://")
        shown = f"{scheme}://***@{rest.partition('@')[2]}"
    print(f"URI:      {shown}")
    print(f"Database: {settings.mongodb_db}")
    print(f"Cache TTL: {settings.doc_cache_ttl_days} days\n")

    store = await connect(settings)
    if store is None:
        print("Could not connect. Is MongoDB running? See docs/mongodb.md.")
        return 1

    stats = await store.stats()
    print("Connected. Indexes ensured.\n")
    print(f"  runs      {stats['runs']:>6}")
    print(f"  plans     {stats['plans']:>6}")
    print(f"  documents {stats['documents']:>6}   (cached pages available for reuse)")

    if stats["documents"]:
        pipeline = [
            {"$project": {"url": 1, "uses": {"$size": {"$ifNull": ["$queries", []]}}}},
            {"$sort": {"uses": -1}},
            {"$limit": 5},
        ]
        print("\nMost reused pages:")
        # pymongo's async aggregate() returns a coroutine yielding the cursor.
        cursor = await store.db["documents"].aggregate(pipeline)
        async for doc in cursor:
            print(f"  {doc['uses']:>3}x  {doc.get('url', doc['_id'])[:70]}")

    await store.close()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
