max_size = 1000
area = [[0]*max_size for i in range(max_size)]
f = open("day5_input.txt", "r")
for i, line in enumerate(f.read().splitlines()):
    coords = line.split(" -> ")
    x1, y1 = list(map(int, coords[0].split(",")))
    x2, y2 = list(map(int, coords[1].split(",")))
    if x1 == x2 or y1 == y2:  # part 1
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for j in range(y1, y2 + 1):
                area[j][x1] += 1
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for j in range(x1, x2 + 1):
                area[y1][j] += 1
    else:  # part 2; comment this 'else' block and the code inside it to get the result for part 1
        if x1 > x2:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        if y2 > y1:
            for j in range(x1, x2 + 1):
                area[y1 + (j - x1)][j] += 1
        else:
            for j in range(x1, x2 + 1):
                area[y1 - (j - x1)][j] += 1

ttl = 0
for i in range(max_size):
    for j in range(max_size):
        if area[i][j] > 1:
            ttl += 1
print("Total is:", ttl)
