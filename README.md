# 🏗️ Cage Rebar Analysis

A web app to upload rebar data (CSV or Excel), analyse it instantly, and download results.

## Features
- Upload CSV or Excel file (supports 1M+ rows)
- Auto-generates **Bar Type** column from Layer logic
- **Dashboard** — KPI cards + charts
- **Cage Summary** — one row per cage with all bar counts
- **Raw Data** — filterable table
- Download any view as CSV or Excel

## File Structure
```
cage-rebar-analysis/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── .streamlit/
    └── config.toml         # Theme & settings
```

## Column Requirements
Your CSV/Excel must have these columns:
- `Layer` — used to calculate Bar Type
- `Correct reference` — cage identifier
- `Bar Type` — auto-added if missing
- `Total Bar Weight` — for weight charts (optional)

## Bar Type Logic
| Layer Prefix | Bar Type |
|---|---|
| F or N | Mesh |
| LK or S | Shear Link |
| LB | Loose Bar |
| VS | VS Sub-Assembly |
| HS | HS Sub-Assembly |
| PRL | Preload |
| Other | Other |
