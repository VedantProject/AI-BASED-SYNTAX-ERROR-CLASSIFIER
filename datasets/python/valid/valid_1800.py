def sum_range(data, y):
    n = 0
    for i in range(data, y + 1):
        n += i
    return n

print(sum_range(10, 18))
