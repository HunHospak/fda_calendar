"""Pure computation for fda_calendar. No I/O, unit-testable."""
from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List, Optional


def _parse_date(s: Any) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(str(s).strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def build_boards(events: Optional[List[Dict[str, Any]]], cfg: Dict[str, Any], today: dt.date) -> Dict[str, Any]:
    if events is None:
        return {
            "as_of": today.isoformat(), "upcoming_count": 0, "upcoming": [], "by_ticker": {},
            "_status": "unavailable", "_notes": "catalysts.yaml could not be read.",
        }

    horizon = today + dt.timedelta(days=int(cfg.get("horizon_days", 180)))
    top_n = int(cfg.get("top_n", 30))

    rows: List[Dict[str, Any]] = []
    for e in events:
        if not isinstance(e, dict):
            continue
        d = _parse_date(e.get("date"))
        if d is None or d < today or d > horizon:
            continue
        rows.append({
            "ticker": (str(e["ticker"]).upper() if e.get("ticker") else None),
            "drug": e.get("drug"),
            "event_type": e.get("event_type"),
            "date": d.isoformat(),
            "days_until": (d - today).days,
            "note": e.get("note"),
        })

    rows.sort(key=lambda r: r["date"])
    upcoming = rows[:top_n]

    by_ticker: Dict[str, Any] = {}
    for r in rows:
        tk = r["ticker"]
        if tk and tk not in by_ticker:  # nearest event per ticker (rows already date-sorted)
            by_ticker[tk] = {"date": r["date"], "event_type": r["event_type"], "days_until": r["days_until"]}

    if not rows:
        status = "partial"
        notes = "No upcoming catalysts configured in catalysts.yaml."
    else:
        status = "active"
        notes = None

    return {
        "as_of": today.isoformat(),
        "horizon_days": int(cfg.get("horizon_days", 180)),
        "upcoming_count": len(rows),
        "upcoming": upcoming,
        "by_ticker": by_ticker,
        "_status": status,
        "_notes": notes,
    }
