import pandas as pd
import os

# Load data
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'cleaned_games.csv')
df = pd.read_csv(csv_path)

# Select key columns for dashboard
dashboard_cols = ['Name', 'Release date', 'owners_mid', 'User score', 'Peak CCU', 'Price', 'Genres', 'Developers', 'successful', 'high_owners', 'high_score', 'high_ccu']
df_dashboard = df[dashboard_cols]

# Explode genres for better analysis
df_dashboard = df_dashboard.explode('Genres')

# Save for PowerBI
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'dashboard_data.csv')
df_dashboard.to_csv(output_path, index=False)
print("Dashboard data exported to", output_path)