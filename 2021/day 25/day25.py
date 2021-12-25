from copy import deepcopy

f = open("day25_input.txt")
lines = f.read().splitlines()
a = []
a_empty = []
for line in lines:
    a_row = []
    a_empty_row = []
    for ch in line:
        a_row.append(ch)
        a_empty_row.append(".")
    a.append(a_row)
    a_empty.append(a_empty_row)

iterations = 0
while True:
    iterations += 1
    moved = 0
    # a_new = deepcopy(a_empty)
    a_copy = deepcopy(a)

    for i in range(len(a) - 1, -1, -1):
        for j in range(len(a[0]) - 1, -1, -1):
            if a[i][j] == ">":
                new_j = j + 1
                if new_j >= len(a[0]):
                    new_j = 0
                if a[i][new_j] == ".":
                    a_copy[i][j] = "."
                    a_copy[i][new_j] = ">"
                    moved += 1
    a = deepcopy(a_copy)

    for i in range(len(a) - 1, -1, -1):
        for j in range(len(a[0]) - 1, -1, -1):
            if a[i][j] == "v":
                new_i = i + 1
                if new_i >= len(a):
                    new_i = 0
                if a[new_i][j] == ".":
                    a_copy[i][j] = "."
                    a_copy[new_i][j] = "v"
                    moved += 1
    a = deepcopy(a_copy)

    if moved == 0:
        break
print("Stopped moving after", iterations, "iterations.")
