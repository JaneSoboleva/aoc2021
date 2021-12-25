f = open("day6_input.txt", "r")
inp = f.read().splitlines()
fishes = list(map(int, inp[0].split(",")))
fish_states = [0] * 9
for fish in fishes:
    fish_states[fish] += 1
for days in range(256):
    newborn = fish_states[0]
    for i in range(8):
        fish_states[i] = fish_states[i + 1]
    fish_states[8] = newborn
    fish_states[6] += newborn
summ = 0
for fish_state in fish_states:
    summ += fish_state
print("Total fishes:", summ)


# old method for part 1, commented out cause it works super slowly for 256 days, because it's a simulation
'''
for days in range(80):
    for i in range(len(fishes)):
        fishes[i] -= 1
        if fishes[i] < 0:
            fishes[i] = 6
            fishes.append(8)
# print("Fish state:", fishes)
print("Total fishes:", len(fishes))
'''