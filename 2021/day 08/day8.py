import itertools

f = open("day8_input.txt")
lines = f.read().splitlines()
count1478 = 0
for line in lines:
    split1 = line.split(" ")
    for i in range(4):
        x = len(split1[-1 - i])
        if x == 2 or x == 3 or x == 4 or x == 7:
            count1478 += 1
print("Count of digits 1/4/7/8 is:", count1478)

# now for the tougher part 2...
# let's say we have 7 segments, represented by [0] * 7 list, and 0 for the unlit segment / 1 for the lit one.
# this is the order:
#  0000
# 1    2
# 1    2
#  3333
# 4    5
# 4    5
#  6666
# and for example, with only indices 3 and 6 lit up it's a "1" digit.
# First, I'll create a set named "dg" of such digits...

dg = [[1, 1, 1, 0, 1, 1, 1], [0, 0, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 0, 1, 1], [0, 1, 1, 1, 0, 1, 0],
      [1, 1, 0, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1, 1], [1, 0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1]]
sb = [['.', 'a'], ['.', 'b'], ['.', 'c'], ['.', 'd'], ['.', 'e'], ['.', 'f'], ['.', 'g']]


def print_digit(value):  # just to verify I didn't mess up anything in "dg" set above
    def print_horizontal(indx):
        c_h = sb[indx][value[indx]]
        print(" " + c_h + c_h + c_h + c_h + " ")

    def print_sides(indx1, indx2):
        c_s1 = sb[indx1][value[indx1]]
        c_s2 = sb[indx2][value[indx2]]
        print(c_s1 + "    " + c_s2)
        print(c_s1 + "    " + c_s2)

    print_horizontal(0)
    print_sides(1, 2)
    print_horizontal(3)
    print_sides(4, 5)
    print_horizontal(6)
    print("----------")


# Checking the output...
# for i in range(10):
#     print_digit(dg[i])
# All good!


# next function returns a digit by lit up lights representation, or -1 if it cannot find one
def check_digit(v):
    for x_i in range(10):
        if v == dg[x_i]:
            return x_i
    return -1

# Checking the output...
# for i in range(10):
#     print(check_digit(dg[i]))
# All good!


# Finally, our "proper" state is abcdefg = 0123456, but it's been messed up randomly.
# So, we'll just have all permutations of abcdefg assigned to 0123456, and whichever works, we accept.
def get_dg_representation(my_perm, s):
    rslt = [0] * 7
    for ch in s:
        rslt[my_perm.index(ch)] = 1
    return rslt


letter_list = list('abcdefg')
total_sum = 0
for line in lines:
    copy_line = line.replace("| ", "")
    split2 = copy_line.split(" ")
    for perm in list(itertools.permutations(letter_list)):
        results = []
        negatives = 0
        for split_elem in split2:
            dg_current = get_dg_representation(list(perm), split_elem)
            dg_obtain = check_digit(dg_current)
            results.append(dg_obtain)
            if dg_obtain == -1:
                negatives = 1
                break
        if negatives == 0:
            final_number = (results[-4] * 1000) + (results[-3] * 100) + (results[-2] * 10) + results[-1]
            total_sum += final_number
            break

print("Total sum for part 2 is:", total_sum)
