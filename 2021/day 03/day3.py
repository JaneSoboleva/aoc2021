max_length = 20
curr_length = 0
zeroes = [0] * max_length
ones = [0] * max_length
input_values = []

with open('day3_input.txt') as openfileobject:
    for line in openfileobject:
        input_values.append(line)  # we need to keep values for part 2
        for i, char in enumerate(line):
            if char == '0':
                zeroes[i] += 1
            elif char == '1':
                ones[i] += 1
            curr_length = i

print("curr_length:", curr_length)
print("Zeroes: ", end='')
for i in range(max_length):
    print(zeroes[i], end=' ')
print("")
print("ZeOnes: ", end='')
for i in range(max_length):
    print(ones[i], end=' ')
print("")

multiplier = 1
num1 = 0
num2 = 0
for i in range(curr_length, -1, -1):
    if zeroes[i] > ones[i]:
        k = 0
    else:
        k = 1
    num1 += (multiplier * k)
    num2 += (multiplier * (1 - k))
    multiplier *= 2

print("num1", num1, "* num2", num2, "=", num1 * num2)


#  --------- part 2 ---------


def exterminator(input_list, position, dispute_resolver):
    f_zeroes = 0
    f_ones = 0
    copy_list = input_list
    for input_item in input_list:
        if input_item[position] == '0':
            f_zeroes += 1
        elif input_item[position] == '1':
            f_ones += 1
    if dispute_resolver == 0:
        to_exterminate = '1' if f_zeroes <= f_ones else '0'
    else:
        to_exterminate = '0' if f_ones >= f_zeroes else '1'
    for x in range(len(copy_list) - 1, -1, -1):
        if copy_list[x][position] == to_exterminate:
            copy_list.pop(x)
    return copy_list


def converter_to_binary(value):
    rslt = 0
    mlt = 1
    for x in range(len(value) - 1, -1, -1):
        if value[x] == '0' or value[x] == '1':
            if value[x] == '1':
                rslt += mlt
            mlt *= 2
    return rslt


print("Clearing up array 1...")
copy_values_1 = input_values.copy()
pst = 0
while len(copy_values_1) > 1:
    copy_values_1 = exterminator(copy_values_1, pst, 0)
    # print(copy_values_1)
    pst += 1

print("Clearing up array 2...")
copy_values_2 = input_values.copy()
pst = 0
while len(copy_values_2) > 1:
    copy_values_2 = exterminator(copy_values_2, pst, 1)
    # print(copy_values_2)
    pst += 1

num01 = converter_to_binary(copy_values_1[0])
num02 = converter_to_binary(copy_values_2[0])
print("num01", num01, "* num02", num02, "=", num01 * num02)
