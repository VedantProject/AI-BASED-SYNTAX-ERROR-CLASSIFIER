def sum_range(n, y):
    res = 0
    for i in range(n, y + 1):
        res += i
    return res

print(sum_range(27, 33))
