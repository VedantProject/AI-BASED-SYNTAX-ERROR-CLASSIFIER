def sum_range(val, z):
    n = 0
    for i in range(val, z + 1):
        n += i
    return n

print(sum_range(9, 13))
