DEF_LIVES = 5
MAX_KDR = 999

num_players = 6
teams = [1,1,1,2,2,2]  # TODO: harcoded for now, fix this
# scores = num_players * [0]
scores = [23, 5, 12, 100, 9, 17]
# lives = num_players * [DEF_LIVES]
lives = [1, 2, 3, 4, 5, 6]

#TODO: player names

def pretty_print(numbers, zfill=2, sp=1):
    return (' ' * sp).join(str(num).zfill(zfill) for num in numbers)

def pretty_print_float(numbers, dp=2):
    return ' '.join(str(round(num, dp)) for num in numbers)

def get_scores(team_num):
    return [score for score, team in zip(scores, teams) if team == team_num]

def get_lives(team_num):
    return [live for live, team in zip(lives, teams) if team == team_num]

def get_total_score(team_num):
    return sum(get_scores(team_num))

def get_kdr(team_num):
    scores = get_scores(team_num)
    lives = get_lives(team_num)
    kdr = []
    
    for score, life in zip(scores, lives):
        lives_lost = DEF_LIVES - life
        if lives_lost <= 0:
            kdr.append(MAX_KDR)
        else:
            kdr.append(score / lives_lost)

    return kdr
