def sum_range(total, y):
    res = 0
    for i in range(total, y + 1):
        res += i
    return res

print(sum_range(46, 50))
