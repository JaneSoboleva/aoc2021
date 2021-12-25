f = open("day12_input.txt")
lines = f.read().splitlines()
dct = {}  # keeping the neighbours' list
vst = {}  # keeping track of cave visits
total_paths = 0  # result
single_small_visited_twice = False  # a flag for part 2, marking whether we've visited a small cave twice
cave_list = []
for line in lines:
    splt = line.split("-")
    cave_list.append(splt[0])
    cave_list.append(splt[1])
cave_list = list(set(cave_list))
for cv_name in cave_list:
    dct[cv_name] = []
    vst[cv_name] = 0
vst["start"] = 2
for line in lines:
    splt = line.split("-")
    dct[splt[0]].append(splt[1])
    dct[splt[1]].append(splt[0])


def visit(cave_name):
    global single_small_visited_twice
    if cave_name == "end":
        global total_paths
        total_paths += 1
        return
    for cave in dct[cave_name]:
        part2_flag = (cave == cave.lower() and vst[cave] == 1 and single_small_visited_twice is False)
        # part2_flag = False  # uncomment for part 1; keep commented for part 2
        if (cave == cave.lower() and vst[cave] == 0) or cave != cave.lower() or part2_flag:
            vst[cave] += 1
            if part2_flag:
                single_small_visited_twice = True
            visit(cave)
            vst[cave] -= 1
            if part2_flag:
                single_small_visited_twice = False


visit("start")
print("There are this many total paths:", total_paths)
