f = open("day23_input2.txt")
lines = f.read().splitlines()
tubes = [[], [], [], []]
tube_targets = ["A", "B", "C", "D"]
corridor = [".", ".", "*", ".", "*", ".", "*", ".", "*", ".", "."]
for i in range(1, len(lines[1]) - 1):
    corridor[i - 1] = lines[1][i]
for i in range(1, 5):
    corridor[i * 2] = "*"
for i in range(2, len(lines)):
    tube_i = -1
    for ch in lines[i]:
        if "A" <= ch <= "D" or ch == ".":
            tube_i += 1
            tubes[tube_i].append(ch)


def is_arranged(tube_status, tube_index):  # check whether the tube only contains units of its type
    for x_i in range(len(tube_status[tube_index])):
        if tube_status[tube_index][x_i] != "." and tube_status[tube_index][x_i] != chr(65 + tube_index):
            return False
    return True


def is_solved(tube_status):
    for x_i in range(4):
        s_ch = chr(65 + x_i)
        for x_j in range(len(tube_status[x_i])):
            if tube_status[x_i][x_j] != s_ch:
                return False
    return True


def check_reachability(corridor_status, corridor_position, tube_index, encounter_limit):
    tube_positions = [2, 4, 6, 8]
    tube_position = tube_positions[tube_index]
    reachable = True
    letters_encountered = 0
    for x_i in range(min(tube_position, corridor_position), max(tube_position, corridor_position) + 1):
        if corridor_status[x_i] != "." and corridor_status[x_i] != "*":
            letters_encountered += 1
            if letters_encountered >= encounter_limit:
                reachable = False
                break
    return reachable, max(tube_position, corridor_position) - min(tube_position, corridor_position) + 1


def not_encountered_yet(tube_status, corridor_status):
    global tube_statuses, corridor_statuses
    return (not (tube_status in tube_statuses)) and (not (corridor_status in corridor_statuses))


def solve(tube_status, corridor_status, energy_spent):
    global max_energy_spent, tube_statuses, corridor_statuses, action_history
    if energy_spent >= max_energy_spent:
        return  # the solution is worse than the best one we found so far
    if is_solved(tube_status):  # didn't get booted out on a previous step; found a better solution than before
        max_energy_spent = energy_spent
        # debug stuff
        print("energy spent updated:", energy_spent)
        # if energy_spent == 12519:
        #     for action_history_line in action_history:
        #         print(action_history_line)
        return

    # tube_status_copy = deepcopy(tube_status)
    # corridor_status_copy = deepcopy(corridor_status)
    tube_status_copy = [[], [], [], []]
    for x_i in range(len(tube_status)):
        for tube_status_item in tube_status[x_i]:
            tube_status_copy[x_i].append(tube_status_item)
    corridor_status_copy = []
    for corridor_status_item in corridor_status:
        corridor_status_copy.append(corridor_status_item)

    # trying to move units from the corridor into their own tube
    for x_i in range(len(corridor_status)):  # checking our corridor
        if "A" <= corridor_status[x_i] <= "D":  # found a unit in the corridor
            tube_index = ord(corridor_status[x_i]) - 65
            if is_arranged(tube_status, tube_index):  # the respective tube is populated properly
                reachable, steps = check_reachability(corridor_status, x_i, tube_index, 2)  # checking reachability
                if reachable:
                    last_ch = corridor_status_copy[x_i]
                    corridor_status_copy[x_i] = "."
                    x_k = 0
                    for x_j in range(len(tube_status[tube_index]) - 1, -1, -1):
                        if tube_status_copy[tube_index][x_j] == ".":
                            x_k = x_j
                            break
                    tube_status_copy[tube_index][x_k] = last_ch
                    new_energy_delta = (x_k + steps) * (10 ** tube_index)
                    new_energy_spent = energy_spent + new_energy_delta
                    if not_encountered_yet(tube_status_copy, corridor_status_copy):
                        tube_statuses.append(tube_status_copy)
                        corridor_statuses.append(corridor_status_copy)
                        action_string = "from corr " + str(x_i) + " into tube " + str(tube_index) + " using " +\
                            str(new_energy_delta) + " energy, total: " + str(new_energy_spent)
                        action_history.append(action_string)
                        solve(tube_status_copy, corridor_status_copy, new_energy_spent)
                        tube_statuses.pop()
                        corridor_statuses.pop()
                        action_history.pop()
                    tube_status_copy[tube_index][x_k] = "."
                    corridor_status_copy[x_i] = last_ch

    # trying to move units from the tubes into the corridor
    for x_i in range(4):  # looping over 4 tubes
        if not is_arranged(tube_status, x_i):  # tube is in disarray, moving from it is allowed
            for x_j in range(len(tube_status[x_i])):  # looping over positions with a letter in them
                if "A" <= tube_status[x_i][x_j] <= "D":  # found a letter
                    for x_k in range(len(corridor_status)):  # looping over available corridor positions
                        if corridor_status[x_k] == ".":  # found an unoccupied place in the corridor
                            reachable, steps = check_reachability(corridor_status, x_k, x_i, 1)  # checking reachability
                            if reachable:  # if reachable, recursively go deeper
                                last_ch = tube_status_copy[x_i][x_j]
                                tube_status_copy[x_i][x_j] = "."
                                corridor_status_copy[x_k] = last_ch
                                new_energy_delta = (x_j + steps) * (10 ** (ord(last_ch) - 65))
                                new_energy_spent = energy_spent + new_energy_delta
                                if not_encountered_yet(tube_status_copy, corridor_status_copy):
                                    tube_statuses.append(tube_status_copy)
                                    corridor_statuses.append(corridor_status_copy)
                                    action_string = "from tube " + str(x_i) + " into corr " + str(x_k) + " using " + \
                                        str(new_energy_delta) + " energy, total: " + str(new_energy_spent)
                                    action_history.append(action_string)
                                    solve(tube_status_copy, corridor_status_copy, new_energy_spent)
                                    tube_statuses.pop()
                                    corridor_statuses.pop()
                                    action_history.pop()
                                tube_status_copy[x_i][x_j] = last_ch
                                corridor_status_copy[x_k] = "."
                    break  # only trying to move the top available unit, we don't need the ones below


tube_statuses = []
corridor_statuses = []
action_history = []
# will append to those two during depth-search, to ensure we don't run into the same position twice
max_energy_spent = 10 ** 9  # we need this assignment before calling solve()
solve(tubes, corridor, 0)
print("Energy spent is:", max_energy_spent)
