# 🏗️ Cage Rebar Analysis

A web app to upload rebar data (CSV or Excel), analyse it instantly, and download results.

## Features
- Upload CSV or Excel file (supports 1M+ rows)
- Auto-generates **Bar Type** column from Layer logic
- **Dashboard** — KPI cards + charts
- **Cage Summary** — one row per cage with all bar counts
- **Raw Data** — filterable table
- Download any view as CSV or Excel

## Live App
> Deployed at: `https://<your-app>.streamlit.app`

---

## Setup on GitHub + Streamlit Cloud (Step by Step)

### Step 1 — Create GitHub Repository
1. Go to [github.com](https://github.com) → Sign in
2. Click **+** (top right) → **New repository**
3. Name it: `cage-rebar-analysis`
4. Set to **Public**
5. Click **Create repository**

### Step 2 — Upload Files
Upload these 3 files to your repo:
- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`

To upload: click **Add file** → **Upload files** in your GitHub repo.

For the `.streamlit/config.toml` file — create a folder called `.streamlit` first:
1. Click **Add file** → **Create new file**
2. Type `.streamlit/config.toml` as the filename
3. Paste the contents of config.toml → **Commit**

### Step 3 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Select your repo: `cage-rebar-analysis`
5. Branch: `main`
6. Main file: `app.py`
7. Click **Deploy** — takes ~2 minutes

### Step 4 — Use the App
1. Open your app URL
2. Upload `Cage_Analysis_Combined.csv` in the sidebar
3. Explore Dashboard, Cage Summary, Raw Data tabs
4. Download results as CSV or Excel

---

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
