fwd = 0
depth = 0  # counted as "aim" for part 2
new_depth = 0

with open('day2_input.txt') as openfileobject:
    for line in openfileobject:
        cmd, nmb = line.split(" ")
        nmb = int(nmb)
        if cmd == "forward":
            fwd += nmb
            new_depth += (nmb * depth)
        if cmd == "down":
            depth += nmb
        if cmd == "up":
            depth -= nmb

print("Depth", depth, "* fwd", fwd, "=", depth * fwd)
print("New depth", new_depth, "* fwd", fwd, "=", new_depth * fwd)
