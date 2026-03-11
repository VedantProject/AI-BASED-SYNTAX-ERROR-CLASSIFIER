def sum_range(count, diff):
    n = 0
    for i in range(count, diff + 1):
        n += i
    return n

print(sum_range(11, 20))
