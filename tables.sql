-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS red_cards;
DROP TABLE IF EXISTS goal_scorers;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS tournaments;

-- Create the tournaments table
CREATE TABLE tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Create the teams table
CREATE TABLE teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    tournament_id INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    goals_scored INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);

-- Create the players table
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    goals INTEGER DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams (id)
);

-- Create the matches table
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    team1_goals INTEGER DEFAULT 0,
    team2_goals INTEGER DEFAULT 0,
    venue TEXT NOT NULL,
    played BOOLEAN DEFAULT 0,
    tournament_id INTEGER NOT NULL,
    FOREIGN KEY (team1_id) REFERENCES teams (id),
    FOREIGN KEY (team2_id) REFERENCES teams (id),
    FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);

-- Create the goal_scorers table
CREATE TABLE goal_scorers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    goals INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players (id),
    FOREIGN KEY (match_id) REFERENCES matches (id)
);

-- Create the red_cards table
CREATE TABLE red_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players (id),
    FOREIGN KEY (match_id) REFERENCES matches (id)
);
