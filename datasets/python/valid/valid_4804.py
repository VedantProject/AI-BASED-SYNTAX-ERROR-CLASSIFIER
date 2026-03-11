def sum_range(z, item):
    n = 0
    for i in range(z, item + 1):
        n += i
    return n

print(sum_range(13, 19))
