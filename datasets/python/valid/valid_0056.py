def sum_range(diff, x):
    res = 0
    for i in range(diff, x + 1):
        res += i
    return res

print(sum_range(16, 23))
