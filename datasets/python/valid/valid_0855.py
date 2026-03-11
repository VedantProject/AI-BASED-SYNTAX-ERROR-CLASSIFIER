def sum_range(val, count):
    n = 0
    for i in range(val, count + 1):
        n += i
    return n

print(sum_range(12, 19))
