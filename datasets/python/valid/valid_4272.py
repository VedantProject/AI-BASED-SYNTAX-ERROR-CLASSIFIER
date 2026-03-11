def sum_range(x, temp):
    n = 0
    for i in range(x, temp + 1):
        n += i
    return n

print(sum_range(29, 33))
