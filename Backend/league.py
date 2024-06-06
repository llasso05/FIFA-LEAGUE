from team import Team
from match import Match

class League:
    def __init__(self):
        self.teams = []
        self.matches = []
        self.goal_scorers = {}

    def add_team(self, team):
        self.teams.append(team)

    def schedule_matches(self):
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match1 = Match(self.teams[i], self.teams[j], self.teams[i].name)
                match2 = Match(self.teams[j], self.teams[i], self.teams[j].name)
                self.matches.append(match1)
                self.matches.append(match2)

    def record_match_result(self, match, team1_goals, team2_goals):
        result = match.record_result(team1_goals, team2_goals)
        self.update_goal_scorers(match.team1, team1_goals)
        self.update_goal_scorers(match.team2, team2_goals)
        return result

    def update_goal_scorers(self, team, goals):
        for player in team.players:
            if player not in self.goal_scorers:
                self.goal_scorers[player] = 0
            self.goal_scorers[player] += goals

    def generate_league_table(self):
        return sorted(self.teams, key=lambda x: (x.points, x.goals_scored - x.goals_against, x.goals_scored), reverse=True)
