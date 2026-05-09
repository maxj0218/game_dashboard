# Steam Game Data Analysis Dashboard
This project uses data scraped from over 120k steam games to determine game success. Data points like price, rating, ownership, publishers/developers, etc are used to compare and predict game success accuracy.

## Local Web Dashboard
A Streamlit-based dashboard is available in `dashboard/app.py`.

To run it locally:

1. Create or activate a Python virtual environment from the project root:
   - Windows PowerShell: `python -m venv .venv` then `& .venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r dashboard/requirements.txt`
3. Start the dashboard:
   - `streamlit run dashboard/app.py`

Open the app in your browser at `http://localhost:8501`.

### What’s included

- `dashboard/app.py` — Streamlit dashboard with overview and modeling pages
- `dashboard/requirements.txt` — Python dependencies for the dashboard
- `data/processed/dashboard_data.csv` — exported dashboard dataset
- `data/processed/cleaned_games.csv` — cleaned dataset used for modeling and clustering

The dashboard includes interactive filters for genres, price, release year, free/paid status, and success status, plus visualizations for genre performance, price vs owners, free vs paid success, and release year trends.

## Data Sources

This project uses the Steam Games Dataset available on Kaggle.

Dataset: Steam Games Dataset  
License: MIT License
Source: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data

The dataset is licensed under the MIT License by its original authors.
All credit for the dataset belongs to the original creators.
