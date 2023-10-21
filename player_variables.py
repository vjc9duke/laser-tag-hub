DEF_LIVES = 5

num_players = 6
teams = [1,1,1,2,2,2]  # TODO: harcoded for now, fix this
scores = num_players * [0]
lives = num_players * [DEF_LIVES]

#TODO: player names

def pretty_print(numbers):
    return ' '.join(str(num).zfill(2) for num in numbers)

def get_scores(team_num):
    return [score for score, team in zip(scores, teams) if team == team_num]

def get_lives(team_num):
    return [live for live, team in zip(lives, teams) if team == team_num]