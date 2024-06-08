class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.players = []
        self.points = 0
        self.goals_scored = 0
        self.goals_against = 0

    def add_player(self, player):
        self.players.append(player)

    def __str__(self):
        return self.name

