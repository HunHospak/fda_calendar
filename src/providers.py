"""Ingest: curated catalysts.yaml. Kept simple and reliable (no fragile scraping).

An automated FDA source can be added later behind the same `gather` interface; for now the
event list is maintained by hand, which is honest and never publishes fabricated dates.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml


def gather(cfg: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    path = root / cfg.get("catalysts_file", "catalysts.yaml")
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {"events": None}  # signals a real error -> unavailable
    events = doc.get("events")
    if not isinstance(events, list):
        events = []
    return {"events": events}
