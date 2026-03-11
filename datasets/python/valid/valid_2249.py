def sum_range(result, b):
    res = 0
    for i in range(result, b + 1):
        res += i
    return res

print(sum_range(7, 12))
