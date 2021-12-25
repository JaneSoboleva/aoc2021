f = open("day14_input.txt")
lines = f.read().splitlines()
orig = lines[0]
starting_pair = orig[0] + orig[1]
ending_pair = orig[-2] + orig[-1]
dct_insert = {}
for i in range(2, len(lines)):
    splt = lines[i].split(" -> ")
    dct_insert[splt[0]] = splt[1]

dct_pairs = {}
lst_pairs = []
for i in range(65, 91):
    for j in range(65, 91):
        dct_pairs[chr(i) + chr(j)] = 0
        lst_pairs.append(chr(i) + chr(j))
for i in range(len(orig) - 1):
    dct_pairs[orig[i] + orig[i + 1]] += 1

for i in range(40):
    # updating starting_pair and ending_pair
    try:
        rp = dct_insert[starting_pair]
    except:
        rp = ""
    if rp != "":
        starting_pair = starting_pair[0] + rp

    try:
        rp = dct_insert[ending_pair]
    except:
        rp = ""
    if rp != "":
        ending_pair = rp + ending_pair[1]

    # doing calculations
    dct_pairs_new = {}
    for i1 in range(65, 91):
        for j1 in range(65, 91):
            dct_pairs_new[chr(i1) + chr(j1)] = 0
    for pair in lst_pairs:
        try:
            rp = dct_insert[pair]
        except:
            rp = ""
        if rp != "":
            pair1 = pair[0] + rp
            pair2 = rp + pair[1]
            dct_pairs_new[pair1] += dct_pairs[pair]
            dct_pairs_new[pair2] += dct_pairs[pair]
            dct_pairs[pair] = 0
    for i1 in range(65, 91):
        for j1 in range(65, 91):
            dct_pairs[chr(i1) + chr(j1)] = dct_pairs_new[chr(i1) + chr(j1)]
    dct_frequency = {}
    for z in range(65, 91):
        dct_frequency[chr(z)] = 0
    for pair in lst_pairs:
        dct_frequency[pair[0]] += dct_pairs[pair]
        dct_frequency[pair[1]] += dct_pairs[pair]
    dct_frequency[starting_pair[0]] += 1
    dct_frequency[ending_pair[-1]] += 1
    for z in range(65, 91):
        dct_frequency[chr(z)] //= 2

    max_score = 0
    for z in range(65, 91):
        if max_score < dct_frequency[chr(z)]:
            max_score = dct_frequency[chr(z)]
    min_score = max_score
    for z in range(65, 91):
        if min_score > dct_frequency[chr(z)] != 0:
            min_score = dct_frequency[chr(z)]

    # debug stuff
    '''
    print(starting_pair + " " + ending_pair + " ", end="")
    print("max_score", max_score, "- min_score", min_score, "=", max_score - min_score, "--- ", end="")
    for pair in lst_pairs:
        if dct_pairs[pair] != 0:
            print(pair + ":" + str(dct_pairs[pair]) + " ", end="")
    print("")
    print(dct_frequency)
    '''
    score = max_score - min_score
    if i == 9:
        print("Score after 10 modifications is:", score)
    if i == 39:
        print("Score after 40 modifications is:", score)
