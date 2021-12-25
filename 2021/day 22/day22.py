from copy import deepcopy

f = open("day22_input.txt")
lines = f.read().splitlines()
input_data = []
for line in lines:
    input_row = []
    splt = line.split()
    if splt[0] == "on":
        input_row.append(1)
    elif splt[0] == "off":
        input_row.append(0)
    elif splt[0] == "break":
        break
    if len(input_row) > 0:
        splt = splt[1].split(",")
        for spl in splt:
            splt2 = spl[2:].split("..")
            input_row.append(int(splt2[0]))
            input_row.append(int(splt2[1]))
        input_data.append(input_row)


def create_3d_list(list_size=10, fill_with=0):
    a_i = []
    for x_i in range(list_size):
        a_j = []
        for x_j in range(list_size):
            a_k = [fill_with] * list_size
            a_j.append(a_k)
        a_i.append(a_j)
    return a_i


def check_result_for_part_1():
    total_lit = 0
    for x_i in range(0, 101):
        for x_j in range(0, 101):
            for x_k in range(0, 101):
                total_lit += h[x_i][x_j][x_k]
    return total_lit


# doing a lazy algo for part 1
h = create_3d_list(list_size=101)

for input_row in input_data:
    range_check = True
    for input_num in input_row:
        if input_num < -50 or input_num > 50:
            range_check = False
    if range_check:
        for i in range(input_row[1] + 50, input_row[2] + 51):
            for j in range(input_row[3] + 50, input_row[4] + 51):
                for k in range(input_row[5] + 50, input_row[6] + 51):
                    h[i][j][k] = input_row[0]
        # print("temporary update (pt1):", check_result_for_part_1())  # some debug to compare with a faulty pt2


print("There are this many activated cubes (part 1):", check_result_for_part_1())


# while part 1 deals with -50..50 cuboid coords, part 2 deals with -100000..100000 cuboid coords
# in that regard, I'm thinking of several solutions...
# Option 1 is to store the cuboids themselves, and smart-split them into non-intersecting ones when the new one appears
# but my head hurts a bit thinking over the algo on how to split them properly

# Option 2 is a more lazy approach, kinda like part 1. First, we make all coordinates positive
# (by adding 5*10^X to all of them, with X big enough to make them all positive)
# then we'd have a [10][10][10] list. list[a][b][c] would have 1, if the entire box of 10^X size is filled,
# 0 if the entire box is not filled, or another [10][10][10] list if filled partially, but for 10^(X-1), etc.
# And it would recursively go down to 10^0. Let's try that...
# UPD: tried that and it didn't go well, trying Option 1 again...


def check_intersection(v1, v2, w1, w2):
    if v2 < w1 or w2 < v1:
        return 0, 0, 0
    if v1 <= w1 <= w2 <= v2:
        return w2 - w1 + 1, w1, w2
    if w1 <= v1 <= v2 <= w2:
        return v2 - v1 + 1, v1, v2
    if v1 <= w1 <= v2 <= w2:
        return v2 - w1 + 1, w1, v2
    if w1 <= v1 <= w2 <= v2:
        return w2 - v1 + 1, v1, w2
    return -1, -1, -1


def remove_cuboid(cub1, cub2):  # order in cub: [x1, x2, y1, y2, z1, z2]; cub2 is the deletion area
    rslt = []
    check_x_sect, cx1, cx2 = check_intersection(cub1[0], cub1[1], cub2[0], cub2[1])
    check_y_sect, cy1, cy2 = check_intersection(cub1[2], cub1[3], cub2[2], cub2[3])
    check_z_sect, cz1, cz2 = check_intersection(cub1[4], cub1[5], cub2[4], cub2[5])
    if check_x_sect == 0 or check_y_sect == 0 or check_z_sect == 0:
        rslt.append(cub1)
        return rslt
    new_x1 = cub1[0]
    new_x2 = cub1[1]
    new_y1 = cub1[2]
    new_y2 = cub1[3]
    if cub1[0] < cub2[0]:
        rslt.append([cub1[0], cub2[0] - 1, cub1[2], cub1[3], cub1[4], cub1[5]])
        new_x1 = cub2[0]
    if cub2[1] < cub1[1]:
        rslt.append([cub2[1] + 1, cub1[1], cub1[2], cub1[3], cub1[4], cub1[5]])
        new_x2 = cub2[1]
    if cub1[2] < cub2[2]:
        rslt.append([new_x1, new_x2, cub1[2], cub2[2] - 1, cub1[4], cub1[5]])
        new_y1 = cub2[2]
    if cub2[3] < cub1[3]:
        rslt.append([new_x1, new_x2, cub2[3] + 1, cub1[3], cub1[4], cub1[5]])
        new_y2 = cub2[3]
    if cub1[4] < cub2[4]:
        rslt.append([new_x1, new_x2, new_y1, new_y2, cub1[4], cub2[4] - 1])
    if cub2[5] < cub1[5]:
        rslt.append([new_x1, new_x2, new_y1, new_y2, cub2[5] + 1, cub1[5]])
    return rslt


def check_result_for_part_2():
    total_volume = 0
    for l_cuboid in stored_cuboids:
        size_x = l_cuboid[1] - l_cuboid[0] + 1
        size_y = l_cuboid[3] - l_cuboid[2] + 1
        size_z = l_cuboid[5] - l_cuboid[4] + 1
        total_volume += (size_x * size_y * size_z)
    return total_volume


# some debug checks
'''
print(remove_cuboid([0, 3, 0, 3, 0, 3], [1, 1, 1, 1, 1, 1]))
print(remove_cuboid([0, 3, 0, 3, 0, 3], [-1, 4, -1, 4, -1, 4]))
print(remove_cuboid([0, 3, 0, 3, 0, 3], [1, 4, 1, 4, 1, 4]))
print(remove_cuboid([0, 3, 0, 3, 0, 3], [-1, 4, 1, 1, 1, 1]))
print(remove_cuboid([0, 3, 0, 3, 0, 3], [0, 3, 0, 3, 1, 3]))
'''


stored_cuboids = []
for input_row in input_data:
    curr_cuboid = input_row.copy()
    operation = curr_cuboid.pop(0)
    stored_cuboids_new = []
    if operation == 0:
        for loop_cuboid in stored_cuboids:
            stored_cuboids_new += remove_cuboid(loop_cuboid, curr_cuboid)
    elif operation == 1:
        for loop_cuboid in stored_cuboids:
            mx_sct, mx1, mx2 = check_intersection(loop_cuboid[0], loop_cuboid[1], curr_cuboid[0], curr_cuboid[1])
            my_sct, my1, my2 = check_intersection(loop_cuboid[2], loop_cuboid[3], curr_cuboid[2], curr_cuboid[3])
            mz_sct, mz1, mz2 = check_intersection(loop_cuboid[4], loop_cuboid[5], curr_cuboid[4], curr_cuboid[5])
            if mx_sct > 0 and my_sct > 0 and mz_sct > 0:
                new_cuboid = [mx1, mx2, my1, my2, mz1, mz2]
                stored_cuboids_new += remove_cuboid(loop_cuboid, new_cuboid)
            else:
                stored_cuboids_new.append(loop_cuboid)
        stored_cuboids_new.append(curr_cuboid)
    stored_cuboids = deepcopy(stored_cuboids_new)
    # print("temporary update (pt2):", check_result_for_part_2())  # debugging part
print("There are this many activated cubes (part 2):", check_result_for_part_2())
