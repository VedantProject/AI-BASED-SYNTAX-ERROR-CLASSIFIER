def sum_range(res, z):
    b = 0
    for i in range(res, z + 1):
        b += i
    return b

print(sum_range(21, 25))
