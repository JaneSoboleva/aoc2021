f = open("day7_input.txt")
lines = f.read().splitlines()
nums = list(map(int, lines[0].split(",")))
min_total_fuel = 10 ** 9
min_total_fuel_2 = 10 ** 9
for i in range(max(nums) + 1):
    curr_ttl = 0
    curr_ttl_2 = 0
    for j in range(len(nums)):
        chg = abs(i - nums[j])
        curr_ttl += chg
        curr_ttl_2 += int(((chg + 1) * chg) / 2)
    if min_total_fuel > curr_ttl:
        min_total_fuel = curr_ttl
    if min_total_fuel_2 > curr_ttl_2:
        min_total_fuel_2 = curr_ttl_2
print("Min total (part 1) is:", min_total_fuel)
print("Min total (part 2) is:", min_total_fuel_2)
