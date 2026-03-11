def sum_range(y, num):
    res = 0
    for i in range(y, num + 1):
        res += i
    return res

print(sum_range(19, 22))
