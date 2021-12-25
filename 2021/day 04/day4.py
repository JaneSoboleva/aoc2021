last_score = 0
first_score = 0
board_count = -1
boards = []
boards_marking = []
board = []
numbers = []

# getting input...
f = open("day4_input.txt", "r")
for i, line in enumerate(f.read().splitlines()):
    if i == 0:
        numbers = list(map(int, line.split(",")))
    elif i % 6 == 1:
        if board_count >= 0:
            boards.append(board)
            # damn, apparently [[0] * 5] * 5 produces something different
            boards_marking.append([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        board_count += 1
        board = []
    else:
        j = (i - 1) % 6 - 1
        board_row = list(map(int, line.split()))
        board.append(board_row)
boards.append(board)
boards_marking.append([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
# print(numbers)
# print(boards)
# print(boards_marking)


# processing...


def mark_board(board_index, board_number):
    # print(boards[board_index])
    # print(board_index)
    for x in range(5):
        for y in range(5):
            if boards[board_index][x][y] == board_number:
                # print(boards_marking)
                boards_marking[board_index][x][y] = 1
                # print(x, y, board_number)
                # print(boards_marking)
                if check_if_wins(board_index):
                    board_total = calculate_score_sum(board_index)
                    mult = board_total * boards[board_index][x][y]
                    # print("board_total", board_total, "* winning number", boards[board_index][x][y], "=", mult)
                    # raise SystemExit  # uncomment to get result for part 1
                    global first_score
                    global last_score
                    global skip_board
                    last_score = mult
                    if first_score == 0:
                        first_score = mult
                    skip_board[board_index] = 1
                    # print(skip_board)
                    return mult


def check_if_wins(board_index):
    for x in range(5):
        if boards_marking[board_index][x][0] + boards_marking[board_index][x][1] + boards_marking[board_index][x][2] + boards_marking[board_index][x][3] + boards_marking[board_index][x][4] == 5:
            print("winner:", boards_marking[board_index])
            return True
        if boards_marking[board_index][0][x] + boards_marking[board_index][1][x] + boards_marking[board_index][2][x] + boards_marking[board_index][3][x] + boards_marking[board_index][4][x] == 5:
            print("winner:", boards_marking[board_index])
            return True
    return False


def calculate_score_sum(board_index):
    board_sum = 0
    for x in range(5):
        for y in range(5):
            if boards_marking[board_index][x][y] == 0:
                board_sum += boards[board_index][x][y]
    return board_sum


skip_board = [0] * len(boards)
for i in range(len(numbers)):
    for j in range(len(boards)):
        if skip_board[j] == 0:
            mark_board(j, numbers[i])

print("first score (part 1) is:", first_score)
print("last score (part 2) is:", last_score)
