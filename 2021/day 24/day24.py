f = open("day24_input.txt")
lines = f.read().splitlines()


def process_instructions(v_input):
    global lines
    dct = {"w": 0, "x": 0, "y": 0, "z": 0}
    if "0" in v_input:
        # print("Input contains a digit 0!")
        return 10 ** 9
    inp_count = -1
    for line_num in range(len(lines)):
        dct_copy = dct.copy()
        splt = lines[line_num].split()
        val2 = 0
        if len(splt) == 0:
            continue
        if splt[0] == "break":
            return dct["z"]
        if splt[0] in ["add", "mul", "div", "mod", "eql"]:
            try:
                val2 = dct[splt[2]]
            except:
                val2 = int(splt[2])
        if splt[0] == "inp":
            inp_count += 1
            try:
                dct[splt[1]] = int(v_input[inp_count])
            except:
                return dct["z"]
        elif splt[0] == "add":
            dct[splt[1]] += val2
        elif splt[0] == "mul":
            dct[splt[1]] *= val2
        elif splt[0] == "div":
            dct[splt[1]] //= val2
        elif splt[0] == "mod":
            dct[splt[1]] %= val2
        elif splt[0] == "eql":
            if dct[splt[1]] == val2:
                dct[splt[1]] = 1
            else:
                dct[splt[1]] = 0
        # if dct_copy != dct:
        #     print("Line", line_num, lines[line_num], "-", dct)
    return dct["z"]


min_z = 10 ** 20
min_i = 0
for i in range(1000, 10000):
    rslt = process_instructions(str(i))
    if min_z > rslt:
        min_z = rslt
        min_i = i
print(min_z, min_i)

min_z = 10 ** 20
min_j = 0
for j in range(1000, 10000):
    rslt = process_instructions(str(min_i * 10000 + j))
    if min_z > rslt:
        min_z = rslt
        min_j = j
print(min_z, min_j)

'''
min_z = 10 ** 20
min_k = 0
for k in range(10 ** 5, 10 ** 6):
    rslt = process_instructions(str(min_i) + str(min_j) + str(k))
    if min_z > rslt:
        min_z = rslt
        min_k = k
print(min_z, min_k, str(min_i) + str(min_j) + str(min_k))
'''

print(process_instructions("36969794979199"))

diff_lines = []
diff_counter = -1
