


def verlet(pos, acc, dt):
    prev_pos = pos
    time = 0

    while pos > 0:
        time += dt
        next_pos = pos * 2 - prev_pos + acc * dt * dt
        prev_pos, pos = pos, next_pos

    return time

for i in [10,100,1000,1000, 10000000, 10000000000]:
    print(1/i, "    ", verlet(100, -9.8, 1/i))
