# x_target = range(20, 31)
# y_target = range(-10, -4)
x_target = range(156, 203)
y_target = range(-110, -68)


def launch_probe(vx, vy):
    global x_target, y_target
    steps = 0
    x = 0
    y = 0
    max_y = 0
    while y > -1000:
        x += vx
        y += vy
        if max_y < y:
            max_y = y
        steps += 1
        vy -= 1
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        if x in x_target and y in y_target:
            return [steps, max_y]
    return [0, max_y]


max_height = -1
max_solutions = 0
# kinda manually handpicked, but whatever
for ax in range(210):
    for ay in range(-111, 210):
        launch_result = launch_probe(ax, ay)
        if launch_result[0] > 0 and max_height < launch_result[1]:
            max_height = launch_result[1]
        if launch_result[0] > 0:
            max_solutions += 1
print("Max height reached is:", max_height)
print("Number of solutions is:", max_solutions)
