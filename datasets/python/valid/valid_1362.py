def sum_range(y, val):
    n = 0
    for i in range(y, val + 1):
        n += i
    return n

print(sum_range(50, 60))
