# Tech Industry Revenue Ranking Report

Generates a PDF report ranking tech companies by annual revenue, pulled from
a Postgres database. Built as a learning exercise around the classic
"generate a report" background-job pattern: query data, render an artifact,
run it as a job (on demand now, scheduled as a stretch goal).

## Stack

- **Postgres 16** (via Docker Compose) — stores company data
- **psycopg2** — queries Postgres from Python
- **ReportLab** — renders the PDF (originally attempted with WeasyPrint —
  see Design Notes below for why that changed)
- **FastAPI** — installed and reserved for wiring up the on-demand job
  endpoint (not yet used — see Status below)

## Setup

1. Start Postgres:
```powershell
   docker compose up -d
```
2. Create a virtual environment and install dependencies:
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install fastapi uvicorn psycopg2-binary reportlab
```
3. Create the table:
```powershell
   docker exec -it assignment5-db-1 psql -U postgres -d techrevenue -c "CREATE TABLE companies (id SERIAL PRIMARY KEY, name TEXT NOT NULL, sector TEXT NOT NULL, revenue NUMERIC NOT NULL, revenue_year INT NOT NULL);"
```
4. Seed the data:
```powershell
   python seed.py
```

## Generating the report (current, manual)

```powershell
python generate_report.py
```

Produces `report.pdf` in the project folder: a title, generation timestamp,
and a table ranking all companies by revenue (highest first), with revenue
abbreviated (e.g. `$638B`). This runs synchronously from the command line —
it is **not yet** a background job or API endpoint.

## Data

20 well-known tech companies, seeded with real, roughly-accurate revenue
figures from each company's most recently reported fiscal year (mostly
FY2024). These are ballpark numbers for demo purposes, not audit-grade — see
`seed.py` for the exact figures used.

## Project structure

- `docker-compose.yml` — Postgres container definition
- `seed.py` — one-time script to populate the `companies` table
- `query_test.py` — throwaway script used to sanity-check the DB connection
  and query before writing the real report logic
- `generate_report.py` — the actual pipeline: `fetch_companies()` queries
  Postgres, `build_pdf()` renders the PDF. Split into two functions
  deliberately, so each can be called independently once wrapped as a job.
- `test_pdf.py` — throwaway script from the WeasyPrint troubleshooting
  attempt; can be deleted, kept here as part of the honest record of what
  was tried.

## Design notes / decisions made along the way

- **WeasyPrint was the original choice** for HTML/CSS-based PDF rendering,
  but it failed at runtime on Windows with `OSError: cannot load library
  'libgobject-2.0-0'`. Its native GTK dependencies (Pango, Cairo, GObject)
  aren't installable via pip and require a separate system-level install
  (e.g. via MSYS2). Rather than go down that path, the project switched to
  **ReportLab**, which has no native dependencies and installs cleanly with
  pip.
  - Trade-off: reports are built with ReportLab's Python API (`Table`,
    `Paragraph`, positioning, styles) instead of HTML/CSS, so layout and
    styling are done in code rather than markup. More verbose, but no
    install fragility.
- Revenue is stored as Postgres `NUMERIC` (not `FLOAT`), which psycopg2
  returns as Python `Decimal` — deliberate, to avoid floating-point
  rounding on monetary values. `format_revenue()` explicitly converts to
  `float` only at display time, for the `$638B`-style abbreviation.
- The "A7 job pattern" referenced in early planning notes turned out to be
  from an unrelated course/context and doesn't apply here — the background
  job (next step) will use a standard, self-chosen pattern instead (likely
  FastAPI `BackgroundTasks` for the on-demand case) rather than following a
  specific prescribed structure.

## Status

- [x] Postgres running in Docker, seeded with 20 companies
- [x] Query layer (`fetch_companies`) working and verified against raw SQL
- [x] PDF generation (`build_pdf`) working, verified visually
- [ ] **Not yet done:** wrap report generation as an actual background job
      triggered on demand (e.g. via a FastAPI endpoint using
      `BackgroundTasks`, returning immediately while the PDF generates
      async, with a way to retrieve the finished file rather than passing
      it around directly)
- [ ] **Stretch, not started:** scheduled/recurring report generation

## Next steps

The immediate next piece of work is the background job wrapper described
above. FastAPI and Uvicorn are already installed in this environment in
anticipation of that step, but no application code (`main.py` or similar)
exists yet.
