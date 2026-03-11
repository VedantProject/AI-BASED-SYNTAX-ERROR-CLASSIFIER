def sum_range(result, size):
    res = 0
    for i in range(result, size + 1):
        res += i
    return res

print(sum_range(37, 47))
