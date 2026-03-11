def sum_range(item, n):
    b = 0
    for i in range(item, n + 1):
        b += i
    return b

print(sum_range(25, 34))
