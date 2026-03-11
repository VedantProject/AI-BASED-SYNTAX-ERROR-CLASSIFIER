def sum_range(a, size):
    res = 0
    for i in range(a, size + 1):
        res += i
    return res

print(sum_range(32, 35))
