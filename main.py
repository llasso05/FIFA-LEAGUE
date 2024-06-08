from team import Team
from player import Player
from league import League
import sqlite3
import random

DATABASE = "fifa_tournament.db"

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    conn = create_connection(DATABASE)
    if conn is not None:
        with open('tables.sql') as f:
            conn.executescript(f.read())
        conn.close()

def insert_tournament(conn, tournament_name):
    """Insert a new tournament into the tournaments table."""
    while True:
        try:
            sql = ''' INSERT INTO tournaments(name) VALUES(?) '''
            cur = conn.cursor()
            cur.execute(sql, (tournament_name,))
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error inserting tournament: {e}")
            tournament_name = input("Please enter a valid tournament name: ")

def insert_team(conn, team, tournament_id):
    """Insert a new team into the teams table."""
    while True:
        try:
            sql = ''' INSERT INTO teams(name, tournament_id, points, goals_scored, goals_against)
                      VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (team.name, tournament_id, team.points, team.goals_scored, team.goals_against))
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error inserting team: {e}")
            team.name = input("Please enter a valid team name: ")

def insert_player(conn, player, team_id):
    """Insert a new player into the players table."""
    while True:
        try:
            sql = ''' INSERT INTO players(name, team_id, goals) VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (player.name, team_id, 0))
            conn.commit()
            break
        except sqlite3.IntegrityError as e:
            print(f"Error inserting player: {e}")
            player.name = input("Please enter a valid player name: ")

def insert_match(conn, match, tournament_id):
    """Insert a new match into the matches table."""
    while True:
        try:
            sql = ''' INSERT INTO matches(team1_id, team2_id, team1_goals, team2_goals, venue, played, tournament_id)
                      VALUES(?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (match.team1.id, match.team2.id, match.team1_goals, match.team2_goals, match.venue, match.played, tournament_id))
            conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error inserting match: {e}")

def record_goal(conn, player_id, match_id, goals):
    """Record a goal for a player in a match."""
    while True:
        try:
            sql = ''' INSERT INTO goal_scorers(player_id, match_id, goals) VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (player_id, match_id, goals))
            conn.commit()
            break
        except sqlite3.IntegrityError as e:
            print(f"Error recording goal: {e}")

def record_red_card(conn, player_id, match_id):
    """Record a red card for a player in a match."""
    while True:
        try:
            sql = ''' INSERT INTO red_cards(player_id, match_id) VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (player_id, match_id))
            conn.commit()
            break
        except sqlite3.IntegrityError as e:
            print(f"Error recording red card: {e}")

def main():
    initialize_database()
    league = League()
    conn = create_connection(DATABASE)

    while True:
        try:
            tournament_name = input("Enter the tournament name: ")
            if not tournament_name.strip():
                raise ValueError("Tournament name cannot be empty.")
            break
        except ValueError as e:
            print(e)
    
    tournament_id = insert_tournament(conn, tournament_name)

    while True:
        try:
            num_teams = int(input("Enter the number of teams: "))
            if num_teams <= 0:
                raise ValueError("Number of teams must be positive.")
            break
        except ValueError as e:
            print(e)
    
    for _ in range(num_teams):
        while True:
            try:
                team_name = input("Enter team name: ")
                if not team_name.strip():
                    raise ValueError("Team name cannot be empty.")
                break
            except ValueError as e:
                print(e)
        
        team = Team(None, team_name)
        team_id = insert_team(conn, team, tournament_id)
        team.id = team_id

        while True:
            try:
                num_players = int(input(f"Enter number of players for {team_name}: "))
                if num_players <= 0:
                    raise ValueError("Number of players must be positive.")
                break
            except ValueError as e:
                print(e)
        
        for _ in range(num_players):
            while True:
                try:
                    player_name = input("Enter player name: ")
                    if not player_name.strip():
                        raise ValueError("Player name cannot be empty.")
                    break
                except ValueError as e:
                    print(e)
            
            player = Player(None, player_name, team_id)
            insert_player(conn, player, team_id)
            player.id = conn.cursor().lastrowid
            team.add_player(player)

        league.add_team(team)

    league.schedule_matches(tournament_id)
    league.display_league_table()

    for match in league.matches:
        print(f"Match: {match.team1.name} vs {match.team2.name} at {match.venue}")
    
    for match in league.matches:
        print(f"\nStarting Match: {match.team1.name} vs {match.team2.name} at {match.venue}")
        
        while True:
            try:
                team1_goals = int(input(f"Enter goals for {match.team1.name}: "))
                if team1_goals < 0:
                    raise ValueError("Goals cannot be negative.")
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                team2_goals = int(input(f"Enter goals for {match.team2.name}: "))
                if team2_goals < 0:
                    raise ValueError("Goals cannot be negative.")
                break
            except ValueError as e:
                print(e)

        result = league.record_match_result(match, team1_goals, team2_goals)
        insert_match(conn, match, tournament_id)
        print(result)
        
        # for player in match.team1.players:
        #     while True:
        #         try:
        #             goals = int(input(f"Enter goals scored by {player.name} for {match.team1.name} (if none, enter 0): "))
        #             if goals < 0:
        #                 raise ValueError("Goals cannot be negative.")
        #             break
        #         except ValueError as e:
        #             print(e)
            
        #     if goals > 0:
        #         record_goal(conn, player.id, match.id, goals)
        
        # for player in match.team2.players:
        #     while True:
        #         try:
        #             goals = int(input(f"Enter goals scored by {player.name} for {match.team2.name} (if none, enter 0): "))
        #             if goals < 0:
        #                 raise ValueError("Goals cannot be negative.")
        #             break
        #         except ValueError as e:
        #             print(e)
            
        #     if goals > 0:
        #         record_goal(conn, player.id, match.id, goals)

        # print(f"\nRecording Red Cards for the match {match.team1.name} vs {match.team2.name}")
        # for player in match.team1.players + match.team2.players:
        #     while True:
        #         try:
        #             red_card = input(f"Did {player.name} receive a red card? (y/n): ").strip().lower()
        #             if red_card not in ['y', 'n']:
        #                 raise ValueError("Invalid input, please enter 'y' or 'n'.")
        #             break
        #         except ValueError as e:
        #             print(e)
            
        #     if red_card == 'y':
        #         record_red_card(conn, player.id, match.id)

    league.display_league_table()

if __name__ == "__main__":
    main()
