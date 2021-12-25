from copy import deepcopy

f = open("day11_input.txt")
lines = f.read().splitlines()
flashes_total = 0
a = []
for line in lines:
    b = []
    for ch in line:
        c = int(ch)
        b.append(c)
    a.append(b)


def pass_time():
    global flashes_total
    new_lst = []
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] += 1
            if a[i][j] >= 10:
                new_lst.append(i * 10 + j)
    while len(new_lst) > 0:
        old_lst = deepcopy(new_lst)
        new_lst = []
        for i in range(len(old_lst)):
            x = old_lst[i] // 10
            y = old_lst[i] % 10
            a[x][y] = -1
            flashes_total += 1
            for i1 in range(-1, 2):
                for i2 in range(-1, 2):
                    if 0 <= x + i1 < len(a) and 0 <= y + i2 < len(a[0]):
                        if a[x + i1][y + i2] >= 0:
                            a[x + i1][y + i2] += 1
                            if a[x + i1][y + i2] >= 10:
                                lst_item = (x + i1) * 10 + (y + i2)
                                if lst_item not in old_lst and lst_item not in new_lst:
                                    new_lst.append(lst_item)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] < 0:
                a[i][j] = 0


time_counter = 0
while True:
    pass_time()
    time_counter += 1
    if time_counter == 100:
        print("There are this many flashes in total after 100 steps:", flashes_total)
    sum_a = 0
    for a_line in a:
        sum_a += sum(a_line)
    if sum_a == 0:
        break
print("Time counter before all octopuses flash is:", time_counter)
