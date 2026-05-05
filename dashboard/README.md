# Steam Games Dashboard

## Setup Instructions

1. Open PowerBI Desktop.

2. Click "Get Data" > "Text/CSV" > Select `data/processed/dashboard_data.csv`.

3. Load the data.

4. Create visualizations:

   - **EDA Tab**: Bar charts for genres vs average owners, scatter plots for price vs owners.

   - **Modeling Tab**: Show model R2, feature importances (export from notebooks).

   - **Clustering Tab**: Scatter plots colored by cluster.

   - **Time Series Tab**: Line chart of average owners by year.

5. Save as `steam_games_dashboard.pbix`.