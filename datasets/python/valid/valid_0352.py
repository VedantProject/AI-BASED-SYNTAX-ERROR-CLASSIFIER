def sum_range(total, b):
    z = 0
    for i in range(total, b + 1):
        z += i
    return z

print(sum_range(36, 39))
