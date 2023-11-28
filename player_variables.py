DEF_LIVES = 5
MAX_KDR = 99

num_players = 4
LORA_id_map = {
    8: 1,
    7: 2,
    1: 3,
    5: 4
}
teams = [1,1,2,2]  # TODO: harcoded for now, fix this
scores = num_players * [0]
# scores = [2,1,0,5]
lives = num_players * [DEF_LIVES]

#TODO: player names

def pretty_print(numbers, zfill=2, sp=5):
    return (' ' * sp).join(str(num).zfill(zfill) for num in numbers)

def pretty_print_float(numbers, dp=2, sp=5):
    return (' ' * sp).join(str(round(num, dp)) for num in numbers)

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
        if score == 0:
            kdr.append(0)
        elif lives_lost <= 0:
            kdr.append(MAX_KDR)
        else:
            kdr.append(score / lives_lost)

    return kdr

def reset():
    global scores, lives
    scores = num_players * [0]
    lives = num_players * [DEF_LIVES]