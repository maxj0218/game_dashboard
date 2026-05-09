# Steam Games Dashboard

## Local Web Dashboard Setup

This project now uses a local Streamlit dashboard instead of PowerBI.

### Run the dashboard

1. From the project root, activate a Python virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `& .venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r dashboard/requirements.txt`
3. Launch the app:
   - `streamlit run dashboard/app.py`

Then open `http://localhost:8501` in your browser.

### Features

- Interactive filtering by genre, price, release year, free/paid, and success status
- Genre performance bar chart
- Price vs owners scatter plot
- Free vs paid success comparison
- Release-year trend line chart
- Top games by estimated owners
- **Modeling & Clustering page** with classification metrics and K-means cluster analysis

### What’s included

- `dashboard/app.py` — Streamlit app for interactive dashboard and modeling insights
- `dashboard/requirements.txt` — dependencies for running the dashboard
- `data/processed/dashboard_data.csv` — prepared dashboard dataset
- `data/processed/cleaned_games.csv` — cleaned game dataset used for modeling

### Data source

Loads prepared dashboard data from `data/processed/dashboard_data.csv`.
