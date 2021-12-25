from copy import deepcopy

f = open("day9_input.txt")
lines = f.read().splitlines()
map_0 = []
for line in lines:
    map_row = []
    for ch in line:
        map_row.append(int(ch))
    map_0.append(map_row)


def check_depth(v1, v2, d1, d2):
    global map_0
    if 0 <= v1 + d1 < len(map_0) and 0 <= v2 + d2 < len(map_0[0]):
        if map_0[v1 + d1][v2 + d2] > map_0[v1][v2]:
            return 1
        else:
            return 0
    else:
        return 1


risk_level = 0
for i in range(len(map_0)):
    for j in range(len(map_0[0])):
        depth_level = 0
        depth_level += check_depth(i, j, -1, 0)
        depth_level += check_depth(i, j, +1, 0)
        depth_level += check_depth(i, j, 0, -1)
        depth_level += check_depth(i, j, 0, +1)
        if depth_level == 4:
            risk_level += map_0[i][j] + 1

print("Total risk level is:", risk_level)


# part 2


def check_basin(v1, v2, d1, d2):
    global visited, new_coords, map_0, curr_sz
    if 0 <= v1 + d1 < len(map_0) and 0 <= v2 + d2 < len(map_0[0]):
        if map_0[v1 + d1][v2 + d2] < 9 and visited[v1 + d1][v2 + d2] == 0:
            new_coord = [v1 + d1, v2 + d2]
            new_coords.append(new_coord)
            visited[v1 + d1][v2 + d2] = 1
            curr_sz += 1


visited = [[0] * len(map_0[0]) for i in range(len(map_0))]
basins = []
for i in range(len(map_0)):
    for j in range(len(map_0[0])):
        if map_0[i][j] < 9 and visited[i][j] == 0:
            curr_sz = 1
            visited[i][j] = 1
            new_coords = [[i, j]]
            while len(new_coords) > 0:
                old_coords = deepcopy(new_coords)
                new_coords = []
                for old_coord in old_coords:
                    check_basin(old_coord[0], old_coord[1], -1, 0)
                    check_basin(old_coord[0], old_coord[1], +1, 0)
                    check_basin(old_coord[0], old_coord[1], 0, -1)
                    check_basin(old_coord[0], old_coord[1], 0, +1)
            basins.append(curr_sz)

basins.sort()
print("Multiple of top 3 basins is:", basins[-1] * basins[-2] * basins[-3])
