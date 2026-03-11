def sum_range(count, total):
    res = 0
    for i in range(count, total + 1):
        res += i
    return res

print(sum_range(23, 33))
