from team import Team
from match import Match
import random

class League:
    def __init__(self):
        self.teams = []
        self.matches = []

    def add_team(self, team):
        self.teams.append(team)

    def schedule_matches(self, tournament_id):
        match_id = 0
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match1 = Match(match_id, self.teams[i], self.teams[j], self.teams[i].name, tournament_id)
                match_id += 1
                match2 = Match(match_id, self.teams[j], self.teams[i], self.teams[j].name, tournament_id)
                match_id += 1
                self.matches.append(match1)
                self.matches.append(match2)
        self.split_season()

    def split_season(self):
        random.shuffle(self.matches)
        half = len(self.matches) // 2
        self.first_half = self.matches[:half]
        self.second_half = self.matches[half:]

    def record_match_result(self, match, team1_goals, team2_goals):
        result = match.record_result(team1_goals, team2_goals)
        return result

    def generate_league_table(self):
        return sorted(self.teams, key=lambda x: (x.points, x.goals_scored - x.goals_against, x.goals_scored), reverse=True)

    def display_league_table(self):
        league_table = self.generate_league_table()
        print("\nLeague Table:")
        for team in league_table:
            print(f"{team.name} - Points: {team.points}, Goals Scored: {team.goals_scored}, Goals Against: {team.goals_against}")
