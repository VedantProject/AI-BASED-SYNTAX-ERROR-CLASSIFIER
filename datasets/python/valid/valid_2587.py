def sum_range(count, temp):
    n = 0
    for i in range(count, temp + 1):
        n += i
    return n

print(sum_range(46, 49))
