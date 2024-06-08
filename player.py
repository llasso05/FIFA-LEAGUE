class Player:
    def __init__(self, id, name, team_id):
        self.id = id
        self.name = name
        self.team_id = team_id
        self.goals = 0

    def __str__(self):
        return self.name
