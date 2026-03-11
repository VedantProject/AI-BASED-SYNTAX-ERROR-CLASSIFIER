def sum_range(b, temp):
    n = 0
    for i in range(b, temp + 1):
        n += i
    return n

print(sum_range(24, 30))
