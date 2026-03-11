def sum_range(y, result):
    n = 0
    for i in range(y, result + 1):
        n += i
    return n

print(sum_range(13, 19))
