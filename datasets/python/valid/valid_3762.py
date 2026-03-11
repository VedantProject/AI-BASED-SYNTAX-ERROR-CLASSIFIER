def sum_range(val, x):
    z = 0
    for i in range(val, x + 1):
        z += i
    return z

print(sum_range(37, 47))
