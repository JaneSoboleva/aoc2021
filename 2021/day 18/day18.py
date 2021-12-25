def parse_expression(v):  # gets a string; returns a list of numbers, a list of their depth, a list of their positions
    v = v + ","
    curr_depth = 0
    last_number = 0
    last_position = 0
    last_char_was_a_digit = False
    number_list = []
    depth_list = []
    position_list = []
    for v_i in range(len(v)):
        v_ch = v[v_i]
        if '0' <= v_ch <= '9':
            if not last_char_was_a_digit:
                last_position = v_i
            last_char_was_a_digit = True
            last_number = last_number * 10 + int(v_ch)
        else:
            if last_char_was_a_digit:
                number_list.append(last_number)
                last_number = 0
                depth_list.append(curr_depth)
                position_list.append(last_position)
            last_char_was_a_digit = False
            if v_ch == "[":
                curr_depth += 1
            elif v_ch == "]":
                curr_depth -= 1
    return number_list, depth_list, position_list


def explode_expression(v):  # returns True, <expression> if explodable (had a pair with a depth 5); otherwise False, v
    v_num, v_depth, v_pos = parse_expression(v)
    v_copy = "" + v
    successfully_processed = False
    for v_i in range(len(v_num)):
        if v_depth[v_i] == 5:
            # found a pair to explode, processing it from right to left (to not mess up the indices)
            if v_i + 2 < len(v_num):  # changing a number to the right
                v_copy = v_copy[:v_pos[v_i + 2]] + ">" + v_copy[v_pos[v_i + 2]:]
                v_copy = v_copy.replace(">" + str(v_num[v_i + 2]), str(v_num[v_i + 2] + v_num[v_i + 1]))
            # replacing a pair in the middle with 0
            v_copy = v_copy[:v_pos[v_i] - 1] + "0" + v_copy[v_pos[v_i + 1] + len(str(v_num[v_i + 1])) + 1:]
            if v_i > 0:  # changing a number to the left
                v_copy = v_copy[:v_pos[v_i - 1]] + "<" + v_copy[v_pos[v_i - 1]:]
                v_copy = v_copy.replace("<" + str(v_num[v_i - 1]), str(v_num[v_i] + v_num[v_i - 1]))
            successfully_processed = True
            break
    return successfully_processed, v_copy


def split_expression(v):  # returns True, <expression> if splittable (had a number >= 10); otherwise False, v
    v_num, v_depth, v_pos = parse_expression(v)
    v_copy = "" + v
    successfully_processed = False
    for v_i in range(len(v_num)):
        if v_num[v_i] >= 10:
            # found a number to split, processing it
            new_num1 = v_num[v_i] // 2
            new_num2 = new_num1
            if new_num2 * 2 < v_num[v_i]:
                new_num2 += 1
            new_str = "[" + str(new_num1) + "," + str(new_num2) + "]"
            v_copy = v_copy[:v_pos[v_i]] + new_str + v_copy[v_pos[v_i] + len(str(v_num[v_i])):]
            successfully_processed = True
            break
    return successfully_processed, v_copy


def calculate_magnitude(v):  # magnutude of [A, B] is 3xA + 2xB, and that needs to be done recursively for all pairs
    v_copy = "" + v
    v_num, v_depth, v_pos = parse_expression(v_copy)
    while len(v_num) > 1:
        for v_i in range(len(v_num) - 1):
            if v_depth[v_i] == v_depth[v_i + 1]:  # found two numbers of the same pair
                v_new = (3 * v_num[v_i]) + (2 * v_num[v_i + 1])
                v_copy = v_copy[:v_pos[v_i] - 1] + str(v_new) + v_copy[v_pos[v_i + 1] + len(str(v_num[v_i + 1])) + 1:]
                break
        v_num, v_depth, v_pos = parse_expression(v_copy)  # suboptimal, but I'm a bit lazy at this point
    return v_num[0]


def reduce_expression(v):  # explode if explodable, otherwise split if splittable, repeat and return the result
    v_copy = "" + v
    while True:
        explode_result, v_copy = explode_expression(v_copy)
        if not explode_result:
            split_result, v_copy = split_expression(v_copy)
            if not split_result:
                break
    return v_copy


def add_expressions(v1, v2):
    return reduce_expression("[" + v1 + "," + v2 + "]")


f = open("day18_input.txt")
lines = f.read().splitlines()
if len(lines) == 0:
    print("Empty file! Exiting.")
    raise SystemExit
sum_so_far = lines[0]
for i in range(1, len(lines)):
    sum_so_far = add_expressions(sum_so_far, lines[i])
print("The final sum is:", sum_so_far)
print("Its magnitude is:", calculate_magnitude(sum_so_far))

# part 2: finding the largest magnitude of the sum between any two expressions (note that x+y and y+x are different)
biggest_magnitude_so_far = calculate_magnitude(lines[0])
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        current_magnitude = calculate_magnitude(add_expressions(lines[i], lines[j]))
        if biggest_magnitude_so_far < current_magnitude:
            biggest_magnitude_so_far = current_magnitude
        current_magnitude = calculate_magnitude(add_expressions(lines[j], lines[i]))
        if biggest_magnitude_so_far < current_magnitude:
            biggest_magnitude_so_far = current_magnitude
print("The biggest magnitude of the sum of two numbers inside the input file is:", biggest_magnitude_so_far)
