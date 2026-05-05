# Steam Game Data Analysis Dashboard
This project uses data scraped from over 120k steam games to determine game success. Data points like price, rating, ownership, publishers/developers, etc are used to compare and predict game success accuracy.

## Implementation Status
- ✅ Data Cleaning and Preparation (`notebooks/01_cleaning_prep.ipynb`)
- ✅ Database Setup and Loading (`data/game_database.db` via `scripts/load_data.py`)
- ✅ Exploratory Data Analysis (`notebooks/02_eda.ipynb`)
- ✅ Predictive Modeling (`notebooks/03_modeling.ipynb`)
- ✅ Clustering and Segmentation (`notebooks/03_modeling.ipynb`)
- ✅ Time Series Analysis (`notebooks/04_time_series.ipynb`)
- ✅ Local Web Dashboard (`dashboard/app.py`)
- ✅ Dashboard data export (`data/processed/dashboard_data.csv`)

## Local Web Dashboard
A Streamlit-based dashboard is available in `dashboard/app.py`.

To run it locally:

1. Install dependencies:
   - `pip install -r dashboard/requirements.txt`
2. Start the dashboard:
   - `streamlit run dashboard/app.py`

The dashboard includes interactive filters for genres, price, release year, and success status, plus visualizations for genre performance, price vs owners, free vs paid success, and release year trends.

## Data Sources

This project uses the Steam Games Dataset available on Kaggle.

Dataset: Steam Games Dataset  
License: MIT License
Source: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data

The dataset is licensed under the MIT License by its original authors.
All credit for the dataset belongs to the original creators.
