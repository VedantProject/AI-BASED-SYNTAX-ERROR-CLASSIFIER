def sum_range(x, num):
    n = 0
    for i in range(x, num + 1):
        n += i
    return n

print(sum_range(36, 44))
