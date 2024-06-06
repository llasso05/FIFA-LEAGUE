class Match:
    def __init__(self, team1, team2, venue):
        self.team1 = team1
        self.team2 = team2
        self.venue = venue
        self.team1_goals = 0
        self.team2_goals = 0
        self.played = False

    def record_result(self, team1_goals, team2_goals):
        self.team1_goals = team1_goals
        self.team2_goals = team2_goals
        self.played = True
        self.update_team_stats()
        return f"Result: {self.team1.name} {team1_goals} - {team2_goals} {self.team2.name}"

    def update_team_stats(self):
        self.team1.goals_scored += self.team1_goals
        self.team1.goals_against += self.team2_goals
        self.team2.goals_scored += self.team2_goals
        self.team2.goals_against += self.team1_goals

        if self.team1_goals > self.team2_goals:
            self.team1.points += 3
        elif self.team2_goals > self.team1_goals:
            self.team2.points += 3
        else:
            self.team1.points += 1
            self.team2.points += 1