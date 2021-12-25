f = open("day10_input.txt")
lines = f.read().splitlines()
total_score = 0
score_2_list = []
for line in lines:
    lst = []
    mod_score = 0
    for ch in line:
        if ch == '(' or ch == '[' or ch == '{' or ch == '<':
            lst.append(ch)
        elif ch == ')' or ch == ']' or ch == '}' or ch == '>':
            if len(lst) == 0:
                last_ch = '^'
            else:
                last_ch = lst.pop()
            if ch == ')' and last_ch != '(':
                mod_score = 3
            elif ch == ']' and last_ch != '[':
                mod_score = 57
            elif ch == '}' and last_ch != '{':
                mod_score = 1197
            elif ch == '>' and last_ch != '<':
                mod_score = 25137
            if mod_score > 0:
                total_score += mod_score
                break
    # part 2
    if mod_score == 0:
        total_score_2 = 0
        h = [0] * 4
        for i in range(len(line) - 1, -1, -1):
            if line[i] == ')':
                h[0] += 1
            elif line[i] == ']':
                h[1] += 1
            elif line[i] == '}':
                h[2] += 1
            elif line[i] == '>':
                h[3] += 1
            elif line[i] == '(':
                h[0] -= 1
            elif line[i] == '[':
                h[1] -= 1
            elif line[i] == '{':
                h[2] -= 1
            elif line[i] == '<':
                h[3] -= 1
            for j in range(4):
                if h[j] < 0:
                    total_score_2 *= 5
                    total_score_2 += (j + 1)
                    h[j] = 0
        score_2_list.append(total_score_2)

print("Total score (part 1) is:", total_score)
score_2_list.sort()
print("Final score (part 2) is:", score_2_list[int(len(score_2_list) / 2)])
