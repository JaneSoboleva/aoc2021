init_player_pos = [7, 9]

# part 1
player_pos = init_player_pos.copy()
player_scores = [0, 0]
curr_player = 0
det_dice_rolls = 0
last_det_dice = 100


def roll_det_dice():
    global last_det_dice, det_dice_rolls
    last_det_dice += 1
    det_dice_rolls += 1
    if last_det_dice > 100:
        last_det_dice = 1
    return last_det_dice


while True:
    moves_to_make = roll_det_dice() + roll_det_dice() + roll_det_dice()
    player_pos[curr_player] += moves_to_make
    player_pos[curr_player] %= 10
    if player_pos[curr_player] == 0:
        player_pos[curr_player] = 10
    player_scores[curr_player] += player_pos[curr_player]
    curr_player = 1 - curr_player
    if max(player_scores) >= 1000:
        print("Game 1 result is:", min(player_scores) * det_dice_rolls)
        break


# part 2
def simulation(score_so_far, player_positions, player_id, score_limit):
    global roll_outcomes
    if max(score_so_far) >= score_limit:
        if score_so_far[0] > score_so_far[1]:
            return [1, 0]
        else:
            return [0, 1]
    wins_so_far = [0, 0]
    for curr_roll in range(3, 10):  # throwing 3 dice of 1..3, we get a 3..9 sum
        player_positions_copy = player_positions.copy()
        score_so_far_copy = score_so_far.copy()
        player_positions_copy[player_id] += curr_roll
        if player_positions_copy[player_id] > 10:
            player_positions_copy[player_id] -= 10
        score_so_far_copy[player_id] += player_positions_copy[player_id]
        next_roll_result = simulation(score_so_far_copy, player_positions_copy, 1 - player_id, score_limit)
        wins_so_far[0] += roll_outcomes[curr_roll] * next_roll_result[0]
        wins_so_far[1] += roll_outcomes[curr_roll] * next_roll_result[1]
    return wins_so_far


roll_outcomes = [0] * 10
for i1 in range(1, 4):
    for i2 in range(1, 4):
        for i3 in range(1, 4):
            roll_outcomes[i1 + i2 + i3] += 1
print("Calculating the result for part 2 (might take a few minutes)...")
print("Player 1 / Player 2 wins:", simulation([0, 0], init_player_pos, 0, 21))
