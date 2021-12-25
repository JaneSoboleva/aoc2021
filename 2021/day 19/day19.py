import random

f = open("day19_input.txt")
lines = f.read().splitlines()
# apparently the scanners can face anywhere... the task text says 24 possible orientations, but isn't it 48?
# with each of 3 coordinates being multiplied either by -1 or +1 (2^3 = 8) and 3 permutations (3! = 6), it's 8*6=48...
# anyways, gotta prepare the modifier data for this... manually, 'cause I don't want the extra code
mult_mods = [[-1, -1, -1], [-1, -1, +1], [-1, +1, -1], [-1, +1, +1],
             [+1, -1, -1], [+1, -1, +1], [+1, +1, -1], [+1, +1, +1]]
perm_mods = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
scanners_raw_data = []  # data from input will be here
scanners_own_coords = []  # initally will have "" in each slot, will be replaced with [x, y, z] when coords are found
probe_coords = []  # like scanners_raw_data, but will have absolute coords instead of relative ones
total_scanners_found = 0
scanner_count = -1
for line in lines:
    splt = line.split(",")
    if splt[0] == "":
        pass
    elif splt[0][-1] == "-":
        scanner_count += 1
        scanners_raw_data.append([])
        scanners_own_coords.append("")
        probe_coords.append("")
    else:
        scanner_coords = [int(splt[0]), int(splt[1]), int(splt[2])]
        scanners_raw_data[scanner_count].append(scanner_coords)

# assuming a default mult_mod and perm_mod for scanner 0; will find data for other scanners as related to this
scanners_own_coords[0] = [0, 0, 0]
# adding absolute probe coords related to scanner 0...
probe_coords[0] = []
for i in range(len(scanners_raw_data[0])):
    v_x = scanners_raw_data[0][i][0]
    v_y = scanners_raw_data[0][i][1]
    v_z = scanners_raw_data[0][i][2]
    probe_coords[0].append([v_x, v_y, v_z])


# now to the actual solution... hmm.
# I'll try to put my idea into words, so that I have something to lean onto while coding further
# I'm assuming the detection is chained (like, we always detect new scanner coords from a previous scanner coords)
# although also maybe not, but that hopefully should not be critical
# let's say we loop over each scanner which doesn't have determined coordinates yet...
# and we make a copy of that scanner, and apply 1 of 48 mult_mod/perm_mod combinations (we also loop over those)
# ...so what we receive is what we assume is the same orientation deltas as scanner 0.
# then we also loop over the available probe coords (or maybe we do it at the start?),
# and finally we loop over the deltas. With that info, we assume the coordinates of the scanner,
# and check if it's correct by finding 12 common probes. Hmmm... To summarize:

# loop over probe coords -> loop over undetermined scanners -> loop over 48 modifications -> loop over scanner deltas
# scanner coords = probe_coords - modified scanner deltas
# with the received coords, check if you have 12 common probes with the scanner you got probe coords from
# With that, I'll be creating a function detect_new_scanner()


def detect_new_scanner(id_to_check):
    global total_scanners_found
    # UPD1: trying to prioritize last ID, which is id_to_check; otherwise give a random order of checking
    id_list = []
    for x_i in range(len(probe_coords)):
        if x_i != id_to_check:
            id_list.append(x_i)
    for x_i in range(len(id_list) - 1, -1, -1):
        x_j = random.randint(0, x_i)
        id_list[x_i], id_list[x_j] = id_list[x_j], id_list[x_i]
    id_list = [id_to_check] + id_list
    for known_scanner_id in id_list:  # 1. loop over...
        for probe_coord in probe_coords[known_scanner_id]:  # ...known probe coords (get [x, y, z] in probe_coord)
            for unknown_scanner_id in range(len(probe_coords)):  # 2. loop over...
                if scanners_own_coords[unknown_scanner_id] == "":  # ...undetermined scanners (got unknown_scanner_id)
                    for curr_mult in range(8):  # 3. loop over...
                        for curr_perm in range(6):  # ...48 modifications
                            for scanner_delta in scanners_raw_data[unknown_scanner_id]:  # 4. loop over scanner detlas
                                curr_delta = scanner_delta.copy()
                                perm_delta = modify_coords(curr_delta, curr_mult, curr_perm)
                                # assuming scanner coords (probe_coord - perm_delta)
                                potential_coords = []
                                for cm in range(3):
                                    potential_coords.append(int(probe_coord[cm]) - perm_delta[cm])
                                # now, knowing known_ and unknown_scanner_id, and potential_coords of a new scanner,
                                # plus curr_mult/curr_perm config, find out how many common beacons they share.
                                # Since the indentation is a bit too deep already, I'll probably make another function!
                                common_num = how_many_common_beacons(known_scanner_id, unknown_scanner_id,
                                                                     potential_coords, curr_mult, curr_perm)
                                if common_num >= 12:  # 12 is required by the task text, we found what we want!
                                    # modify scanners_raw_data[unknown_scanner_id] using curr_mult and curr_perm
                                    total_scanners_found += 1
                                    print("Found a new scanner #" + str(total_scanners_found) + ":", potential_coords)
                                    for x_i in range(len(scanners_raw_data[unknown_scanner_id])):
                                        scanners_raw_data[unknown_scanner_id][x_i] = \
                                            modify_coords(scanners_raw_data[unknown_scanner_id][x_i],
                                                          curr_mult, curr_perm)
                                    # set new coords
                                    scanners_own_coords[unknown_scanner_id] = potential_coords.copy()
                                    # set new probe coords based on a newfound scanner position
                                    probe_coords[unknown_scanner_id] = []
                                    for scanner_new_delta in scanners_raw_data[unknown_scanner_id]:
                                        scanner_append_delta = []
                                        for x_i in range(3):
                                            scanner_append_delta.append(scanners_own_coords[unknown_scanner_id][x_i] +
                                                                        scanner_new_delta[x_i])
                                        probe_coords[unknown_scanner_id].append(scanner_append_delta)
                                    # It's finally done and let's hope it all works correctly once I test it...
                                    # UPD1: it works, but too slowly, if I just loop all.
                                    # I'll try prioritizing the last_id for the search...
                                    return unknown_scanner_id


def modify_coords(v_coords, v_mult, v_perm):  # modifies coords according to mult and perm
    global mult_mods, perm_mods
    # modify according to curr_mult
    curr_result = v_coords.copy()
    for cm in range(3):
        curr_result[cm] *= mult_mods[v_mult][cm]
    # modify according to curr_perm
    final_result = []
    for cm in range(3):
        final_result.append(curr_result[perm_mods[v_perm][cm]])
    return final_result


def how_many_common_beacons(known_id, unknown_id, v_coords, v_mult, v_perm):
    rslt = 0
    for scanner_new_delta in scanners_raw_data[unknown_id]:
        scanner_changed_delta = modify_coords(scanner_new_delta, v_mult, v_perm)
        scanner_append_delta = []
        for x_i in range(3):
            scanner_append_delta.append(v_coords[x_i] + scanner_changed_delta[x_i])
        if scanner_append_delta in probe_coords[known_id]:
            rslt += 1
    return rslt


# phew... final part of the program
last_known_id = 0
for i in range(len(scanners_own_coords) - 1):
    last_known_id = detect_new_scanner(last_known_id)

final_probe_coords = []
for i in range(len(probe_coords)):
    for probe_c in probe_coords[i]:
        if not (probe_c in final_probe_coords):
            final_probe_coords.append(probe_c)
print("There are this many unique beacon coords:", len(final_probe_coords))

# part 2: largest distance between scanners. Thank god it's easy.

largest_dist = 0
for i in range(len(scanners_own_coords)):
    for j in range(len(scanners_own_coords)):
        curr_dist = 0
        curr_dist += abs(scanners_own_coords[i][0] - scanners_own_coords[j][0])
        curr_dist += abs(scanners_own_coords[i][1] - scanners_own_coords[j][1])
        curr_dist += abs(scanners_own_coords[i][2] - scanners_own_coords[j][2])
        if largest_dist < curr_dist:
            largest_dist = curr_dist
print("The largest distance between scanners is:", largest_dist)
