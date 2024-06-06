from team import Team
from league import League
import sqlite3
import random

DATABASE = "fifa_league.db"

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# def initialize_database():
#     """Initialize the database and create tables if they don't exist."""
#     conn = create_connection(DATABASE)
#     if conn is not None:
#         with open('create_fifa_tournament.sql') as f:
#             conn.executescript(f.read())
#         conn.close()

def insert_team(conn, team):
    """Insert a new team into the teams table."""
    sql = ''' INSERT INTO teams(name, points, goals_scored, goals_against)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (team.name, team.points, team.goals_scored, team.goals_against))
    conn.commit()
    return cur.lastrowid

def insert_player(conn, player, team_id):
    """Insert a new player into the players table."""
    sql = ''' INSERT INTO players(name, team_id, goals)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (player, team_id, 0))
    conn.commit()

def main():
    # initialize_database()
    league = League()

    while True:
        print("\n1. Start a new tournament")
        print("2. View last tournament results")
        choice = input("Enter your choice: ")

        if choice == '1':
            num_teams = int(input("Enter the number of teams: "))
            conn = create_connection(DATABASE)

            for _ in range(num_teams):
                team_name = input("Enter team name: ")
                team = Team(team_name)
                team_id = insert_team(conn, team)

                num_players = int(input(f"Enter number of players for {team_name}: "))
                for _ in range(num_players):
                    player_name = input("Enter player name: ")
                    team.add_player(player_name)
                    insert_player(conn, player_name, team_id)

                league.add_team(team)

            league.schedule_matches()
            league.display_league_table()

            # Record match results
            for match in league.matches:
                team1_goals = int(input(f"Enter goals for {match.team1.name} in match against {match.team2.name}: "))
                team2_goals = int(input(f"Enter goals for {match.team2.name} in match against {match.team1.name}: "))
                result = league.record_match_result(match, team1_goals, team2_goals)
                print(result)
                league.display_league_table()

            conn.close()

        elif choice == '2':
            conn = create_connection(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT name, points, goals_scored, goals_against FROM teams ORDER BY points DESC, (goals_scored - goals_against) DESC, goals_scored DESC")
            rows = cur.fetchall()
            print("\nLast Tournament Results:")
            for row in rows:
                print(f"Team: {row[0]}, Points: {row[1]}, Goals Scored: {row[2]}, Goals Against: {row[3]}")
            conn.close()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
