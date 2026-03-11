def sum_range(n, count):
    res = 0
    for i in range(n, count + 1):
        res += i
    return res

print(sum_range(24, 27))
