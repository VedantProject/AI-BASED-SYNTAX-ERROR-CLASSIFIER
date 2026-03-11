def sum_range(diff, z):
    res = 0
    for i in range(diff, z + 1):
        res += i
    return res

print(sum_range(26, 29))
