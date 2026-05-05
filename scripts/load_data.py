import pandas as pd
import sqlite3
import os

# Database connection
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'game_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    AppID INTEGER PRIMARY KEY,
    Name TEXT,
    Release_date TEXT,
    Estimated_owners TEXT,
    Peak_CCU INTEGER,
    Required_age INTEGER,
    Price REAL,
    DLC_count INTEGER,
    Supported_languages TEXT,
    Windows INTEGER,
    Mac INTEGER,
    Linux INTEGER,
    Metacritic_score REAL,
    User_score REAL,
    Positive INTEGER,
    Negative INTEGER,
    Score_rank TEXT,
    Achievements INTEGER,
    Recommendations INTEGER,
    Average_playtime_forever REAL,
    Median_playtime_forever REAL,
    Developers TEXT,
    Publishers TEXT,
    Genres TEXT,
    Categories TEXT,
    owners_low INTEGER,
    owners_high INTEGER,
    owners_mid REAL,
    high_owners INTEGER,
    high_score INTEGER,
    high_ccu INTEGER,
    successful INTEGER
)
''')

# Load data
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'cleaned_games.csv')
df = pd.read_csv(csv_path)

# Convert lists to strings for storage
df['Genres'] = df['Genres'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
df['Categories'] = df['Categories'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
df['Developers'] = df['Developers'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
df['Publishers'] = df['Publishers'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

# Convert boolean to int
bool_cols = ['Windows', 'Mac', 'Linux', 'high_owners', 'high_score', 'high_ccu', 'successful']
for col in bool_cols:
    df[col] = df[col].astype(int)

# Insert data
df.to_sql('games', conn, if_exists='replace', index=False)

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully!")