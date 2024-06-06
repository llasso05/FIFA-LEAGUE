from team import Team
from Backend.league import League

def main():
    # Create an instance of the League
    league = League()

    # Create instances of Team
    team1 = Team("Team 1")
    team2 = Team("Team 2")

    # Add players to the teams
    team1.add_player("Player 1A")
    team1.add_player("Player 1B")
    team2.add_player("Player 2A")
    team2.add_player("Player 2B")

    # Add teams to the league
    league.add_team(team1)
    league.add_team(team2)

    # Schedule matches
    league.schedule_matches()

    # Record a match result
    match = league.matches[0]
    result = league.record_match_result(match, 2, 1)
    print(result)  # Output: Result: Team 1 2 - 1 Team 2

    # Generate and print the league table
    league_table = league.generate_league_table()
    for team in league_table:
        print(f"{team.name} - Points: {team.points}, Goals Scored: {team.goals_scored}, Goals Against: {team.goals_against}")

if __name__ == "__main__":
    main()
