def sum_range(item, diff):
    z = 0
    for i in range(item, diff + 1):
        z += i
    return z

print(sum_range(28, 38))
