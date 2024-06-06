import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    database = "fifa_tournament.db"

    sql_create_teams_table = """
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        points INTEGER DEFAULT 0,
        goals_scored INTEGER DEFAULT 0,
        goals_against INTEGER DEFAULT 0
    );"""

    sql_create_players_table = """
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        team_id INTEGER NOT NULL,
        goals INTEGER DEFAULT 0,
        FOREIGN KEY (team_id) REFERENCES teams (id)
    );"""

    sql_create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team1_id INTEGER NOT NULL,
        team2_id INTEGER NOT NULL,
        team1_goals INTEGER DEFAULT 0,
        team2_goals INTEGER DEFAULT 0,
        venue TEXT NOT NULL,
        played BOOLEAN DEFAULT 0,
        FOREIGN KEY (team1_id) REFERENCES teams (id),
        FOREIGN KEY (team2_id) REFERENCES teams (id)
    );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_teams_table)
        create_table(conn, sql_create_players_table)
        create_table(conn, sql_create_matches_table)
        print("Tables created successfully.")
    else:
        print("Error! Cannot create the database connection.")

    if conn:
        conn.close()

if __name__ == "__main__":
    main()
