def sum_range(total, z):
    res = 0
    for i in range(total, z + 1):
        res += i
    return res

print(sum_range(21, 24))
