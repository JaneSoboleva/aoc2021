count = 0
count2 = 0
last = 100500
sum3 = 0
arr = [0, 0, 0]

with open('day1_input.txt') as openfileobject:
    counter = -1
    for line in openfileobject:
        counter += 1
        v = int(line)
        if counter < 3:
            arr[counter] = v
        else:
            sum1 = arr[0] + arr[1] + arr[2]
            sum2 = arr[1] + arr[2] + v
            if sum2 > sum1:
                count2 += 1
            arr[0] = arr[1]
            arr[1] = arr[2]
            arr[2] = v

        if v > last:
            count += 1
            last = v
        else:
            last = v


print("Count (puzzle 1) is:", count)
print("Count (puzzle 2) is:", count2)
