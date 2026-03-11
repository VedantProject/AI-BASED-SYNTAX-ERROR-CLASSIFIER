def sum_range(res, size):
    n = 0
    for i in range(res, size + 1):
        n += i
    return n

print(sum_range(22, 32))
