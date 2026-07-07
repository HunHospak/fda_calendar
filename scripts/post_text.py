"""Generate a ready-to-post social snippet from the latest feed."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    feed = json.loads((ROOT / "out" / "fda_calendar.json").read_text(encoding="utf-8"))
    d = feed["data"]
    lines = [f"FDA catalysts — next {d.get('horizon_days')}d ({d.get('as_of')})"]
    up = d.get("upcoming", [])[:5]
    if up:
        for x in up:
            tk = (x.get("ticker") + " ") if x.get("ticker") else ""
            lines.append(f"  {x['date']}  {tk}{x.get('event_type','')}  ({x['days_until']}d)")
    else:
        lines.append("No upcoming catalysts on the calendar.")
    lines.append("Curated regulatory calendar · not investment advice · arkenlabs.eu")
    text = "\n".join(lines)
    (ROOT / "out" / "post.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
