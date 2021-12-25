from copy import deepcopy

f = open("day15_input.txt")
lines = f.read().splitlines()
a = []
r = []
b = []
r1 = []
for line in lines:
    b = []
    r1 = []
    for ch in line:
        b.append(int(ch))
        r1.append(10 ** 9)
    a.append(b)
    r.append(r1)
r[0][0] = 0


def solve():
    global a, r
    new_coords = [[0, 0]]
    while len(new_coords) > 0:
        old_coords = deepcopy(new_coords)
        new_coords = []
        c_mod = [-1, 0, +1]
        for z in range(len(old_coords)):
            x, y = old_coords[z][0], old_coords[z][1]
            for m1 in c_mod:
                for m2 in c_mod:
                    if 0 <= x + m1 < len(a) and 0 <= y + m2 < len(b) and (m1 == 0 or m2 == 0):
                        a_num = int(a[x + m1][y + m2])
                        if r[x][y] + a_num < r[x + m1][y + m2]:
                            new_coord = [x + m1, y + m2]
                            new_coords.append(new_coord)
                            r[x + m1][y + m2] = r[x][y] + a_num
    print("The lowest risk level is:", r[len(a) - 1][len(b) - 1])


def enlarge_your_map():
    global a, r
    a1 = deepcopy(a)
    for i in range(1, 5):
        for j in range(len(a1)):
            for num_a1 in a1[j]:
                new_num = num_a1 + i
                if new_num >= 10:
                    new_num -= 9
                a[j].append(new_num)
    a1 = deepcopy(a)
    for i in range(1, 5):
        for j in range(len(a1)):
            k = deepcopy(a1[j])
            for g in range(len(k)):
                k[g] += i
                if k[g] >= 10:
                    k[g] -= 9
            a.append(k)
    r = []
    for i in range(len(a)):
        rr1 = []
        for j in range(len(a[0])):
            rr1.append(10 ** 9)
        r.append(rr1)
    r[0][0] = 0


solve()
enlarge_your_map()
solve()
