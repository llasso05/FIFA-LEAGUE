# the league project 

# Class Team
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.points = 0
        self.goals_scored = 0
        self.goals_against = 0

    def add_player(self, player_name):
        self.players.append(player_name)
        return f"Player {player_name} added to team {self.name}"




        
