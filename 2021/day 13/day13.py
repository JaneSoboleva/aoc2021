f = open("day13_input.txt")
lines = f.read().splitlines()
max_x = 0
max_y = 0
coords_x = []
coords_y = []
folds_axis = []
folds_coord = []
for line in lines:
    splt = line.split(",")
    if len(splt) > 1:
        curr_x = int(splt[0])
        curr_y = int(splt[1])
        coords_x.append(curr_x)
        coords_y.append(curr_y)
        if max_x < curr_x:
            max_x = curr_x
        if max_y < curr_y:
            max_y = curr_y
    else:
        splt = line.split("=")
        if len(splt) == 1:
            continue
        folds_coord.append(int(splt[1]))
        if splt[0][-1] == 'x':
            folds_axis.append(1)
        else:
            folds_axis.append(0)

a = [[0] * (max_x + 1) for i in range(max_y + 1)]
for z in range(len(coords_x)):
    a[coords_y[z]][coords_x[z]] = 1


def vertical_fold(coord):
    global max_x, max_y, a
    for j in range(coord + 1, max_x + 1):
        for i in range(max_y + 1):
            if a[i][j] == 1:
                a[i][coord - (j - coord)] = 1
    max_x = coord - 1


def horizontal_fold(coord):
    global max_x, max_y, a
    for j in range(coord + 1, max_y + 1):
        for i in range(max_x + 1):
            if a[j][i] == 1:
                a[coord - (j - coord)][i] = 1
    max_y = coord - 1


def count_dots():
    global a
    rslt = 0
    for i in range(max_y + 1):
        for j in range(max_x + 1):
            rslt += a[i][j]
    return rslt


def print_map():
    global a
    for i in range(max_y + 1):
        for j in range(max_x + 1):
            if a[i][j] == 0:
                print(".", end="")
            else:
                print("#", end="")
        print("")
    print("")
    print("----------")
    print("")


# print_map()
for z in range(len(folds_axis)):
    if folds_axis[z] == 0:
        horizontal_fold(folds_coord[z])
    else:
        vertical_fold(folds_coord[z])
    if z == 0:
        print("There are this many visible dots:", count_dots())
    # print_map()
print_map()
