def get_reading(v, x_i, x_j, printing=True):
    x_s = ""
    for x_i1 in range(-1, 2):
        for x_j1 in range(-1, 2):
            x_s += v[x_i + x_i1][x_j + x_j1]
    g2 = 1
    indx = 0
    for x_i1 in range(len(x_s) - 1, -1, -1):
        if x_s[x_i1] == "#":
            indx += g2
        g2 *= 2
    rslt = fltr[indx]
    if printing:
        print(rslt, end="")
    return rslt


def process_image(v, printing=True):
    global fltr, modifier_flag
    pixels_lit = 0
    v_res = []
    for x_i in range(len(v)):
        v_res_row = []
        for x_j in range(len(v[0])):
            v_res_row.append(".")
        v_res.append(v_res_row)
    for x_i in range(1, len(v) - 1):
        for x_j in range(1, len(v[0]) - 1):
            rslt = get_reading(v, x_i, x_j, printing=False)
            v_res[x_i][x_j] = rslt
            if rslt == "#":
                pixels_lit += 1
        # if printing:
        #     print("")
    # remove 1 layer
    v_res.pop(0)
    v_res.pop()
    for x_i in range(len(v_res)):
        v_res[x_i].pop(0)
        v_res[x_i].pop()
    pixel_lit_backup = 0
    if printing:
        print("Pixels lit:", pixels_lit)
        for x_i in range(len(v_res)):
            for x_j in range(len(v_res[0])):
                print(v_res[x_i][x_j], end="")
                if v_res[x_i][x_j] == "#":
                    pixel_lit_backup += 1
            print("")
        print("Pixel lit backup:", pixel_lit_backup, "and pixel lit is:", pixels_lit)
    modifier_flag = not modifier_flag  # keeps track of whether to fill the infinite map with .s or #s
    return v_res, pixels_lit


def add_two_layers(v):
    v_rslt = []
    dot_row = []
    v_ch = '.'
    global modifier_flag, fltr
    if not modifier_flag and fltr[0] == "#":
        v_ch = '#'
    for x_i in range(len(v[0]) + 4):
        dot_row.append(v_ch)
    v_rslt.append(dot_row)
    v_rslt.append(dot_row)
    for x_i in range(len(v)):
        new_row = [v_ch, v_ch] + v[x_i] + [v_ch, v_ch]
        v_rslt.append(new_row)
    v_rslt.append(dot_row)
    v_rslt.append(dot_row)
    return v_rslt


f = open("day20_input.txt")
lines = f.read().splitlines()
fltr = lines[0]
modifier_flag = True
my_img = []
for i in range(2, len(lines)):
    my_row = []
    for ch in lines[i]:
        my_row.append(ch)
    my_img.append(my_row)

pxl_lit = 0
for i in range(2):
    my_img = add_two_layers(my_img)
    my_img, pxl_lit = process_image(my_img, printing=False)
print("Total pixels lit (part 1):", pxl_lit)
for i in range(48):
    my_img = add_two_layers(my_img)
    my_img, pxl_lit = process_image(my_img, printing=False)
print("Total pixels lit (part 2):", pxl_lit)
