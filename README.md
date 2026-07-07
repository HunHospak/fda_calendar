# fda_calendar

Independent ArkenLabs satellite. Publishes upcoming FDA / regulatory catalysts (PDUFA dates,
advisory-committee meetings, readouts). Fully decoupled — the app fetches it read-only.

## Produces `out/fda_calendar.json`

`data`:
- `upcoming` — sorted soonest-first: `{ticker, drug, event_type, date, days_until, note}`
- `by_ticker` — nearest event per symbol, for the company page

## How the data is maintained

Events live in **`catalysts.yaml`** and are curated by hand from the FDA advisory-committee
calendar and company IR / PDUFA target dates. This is intentional: it never publishes
fabricated dates. The feed publishes as `status: "partial"` while the list is empty.

An automated FDA ingestion can later be dropped in behind the same `gather()` interface
without touching the app.

```yaml
events:
  - ticker: SRPT
    drug: "Example program"
    event_type: PDUFA        # PDUFA | AdComm | Readout | Other
    date: "2026-09-30"
    note: "PDUFA target action date"
```

## Run locally

```bash
pip install -r requirements.txt
python src/build_feed.py && python scripts/post_text.py
```

## Publish

GitHub Actions publishes `out/` to `gh-pages` (weekdays + manual dispatch). No secrets.

## Not investment advice

Curated informational calendar.
