-- SQLite setup
-- Database file will be created at data/game_database.db

-- Table creation
CREATE TABLE IF NOT EXISTS games (
    AppID INTEGER PRIMARY KEY,
    Name TEXT,
    Release_date TEXT,  -- SQLite uses TEXT for dates
    Estimated_owners TEXT,
    Peak_CCU INTEGER,
    Required_age INTEGER,
    Price REAL,
    DLC_count INTEGER,
    Supported_languages TEXT,
    Windows INTEGER,  -- SQLite uses INTEGER for BOOLEAN
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
);