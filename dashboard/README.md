# Steam Games Dashboard

## Local Web Dashboard Setup

This project now uses a local Streamlit dashboard instead of PowerBI.

### Run the dashboard

1. Install dependencies:
   - `pip install -r dashboard/requirements.txt`

2. Launch the app:
   - `streamlit run dashboard/app.py`

### Features

- Interactive filtering by genre, price, release year, free/paid, and success status
- Genre performance bar chart
- Price vs owners scatter plot
- Free vs paid success comparison
- Release-year trend line chart
- Top games by estimated owners
- **Modeling & Clustering page** with classification metrics and K-means cluster analysis

### Data source

Loads prepared dashboard data from `data/processed/dashboard_data.csv`.
