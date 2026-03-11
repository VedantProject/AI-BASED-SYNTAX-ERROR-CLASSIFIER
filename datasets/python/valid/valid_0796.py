def sum_range(diff, num):
    res = 0
    for i in range(diff, num + 1):
        res += i
    return res

print(sum_range(32, 34))
