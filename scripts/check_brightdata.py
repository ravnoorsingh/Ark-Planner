"""Probe the Bright Data collector and print the exact shape of a returned row.

A Scraper Studio collector's output schema is whatever was defined when it was
built, so the field holding page content cannot be known ahead of time. Run this
once against your collector to see the real keys, then set
BRIGHT_DATA_CONTENT_FIELD if auto-detection picked the wrong one.

    uv run python scripts/check_brightdata.py https://fastapi.tiangolo.com
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from ark.brightdata import (
    CONTENT_FIELD_CANDIDATES,
    BrightDataError,
    looks_like_html,
    pick_content_field,
    row_to_markdown,
    scrape_urls,
)
from ark.config import MissingCredentials, load_settings

DEFAULT_URL = "https://fastapi.tiangolo.com"


async def main() -> int:
    load_dotenv()
    settings = load_settings()
    needed = ["BRIGHT_DATA_API_TOKEN"]
    if settings.scrape_backend == "collector":
        needed.append("BRIGHT_DATA_COLLECTOR_ID")
    try:
        settings.require_credentials(*needed)
    except MissingCredentials as exc:
        print(exc)
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    print(f"Backend:   {settings.scrape_backend}")
    if settings.scrape_backend == "collector":
        print(f"Collector: {settings.brightdata_collector_id}")
    else:
        print(f"Zone:      {settings.brightdata_unlocker_zone}")
    print(f"Probing:   {url}\n")

    def on_tick(remaining: float) -> None:
        print(f"  … still building ({remaining:.0f}s before timeout)")

    try:
        rows = await scrape_urls(settings, [url], on_tick=on_tick)
    except BrightDataError as exc:
        print(f"FAILED: {exc}")
        return 1

    row = rows.get(url)
    if row is None:
        print("The collector returned no row for that URL.")
        print("Check the collector's Runs tab in Scraper Studio for the failure reason.")
        return 1

    # Save before any early return, so the file always matches this probe rather
    # than leaving a stale row from a previous run to be misread.
    row_path = Path(__file__).with_name("_last_brightdata_row.json")
    row_path.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Row keys and value types:")
    for key, value in row.items():
        preview = ""
        if isinstance(value, str):
            preview = f"  {len(value)} chars"
            if looks_like_html(value):
                preview += " (looks like HTML)"
        print(f"  • {key:<20} {type(value).__name__}{preview}")

    override = settings.brightdata_content_field
    field = pick_content_field(row, override)
    print()
    if override:
        print(f"BRIGHT_DATA_CONTENT_FIELD is set to {override!r}.")
        if field is None:
            print(f"  !! That field is missing or empty in this row. Keys: {sorted(row)}")
            return 1
    elif field is None:
        print("No content field auto-detected.")
        print(f"  Tried: {', '.join(CONTENT_FIELD_CANDIDATES)}")
        print(f"  Set BRIGHT_DATA_CONTENT_FIELD to one of: {sorted(row)}")
        return 1
    else:
        print(f"Auto-detected content field: {field!r}")

    markdown = row_to_markdown(row, override)
    print(f"Markdown length: {len(markdown)} chars\n")
    print("--- first 600 chars " + "-" * 40)
    print(markdown[:600])
    print("-" * 60)

    print(f"\nFull row saved to {row_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
