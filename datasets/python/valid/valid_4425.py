def sum_range(val, item):
    z = 0
    for i in range(val, item + 1):
        z += i
    return z

print(sum_range(37, 46))
