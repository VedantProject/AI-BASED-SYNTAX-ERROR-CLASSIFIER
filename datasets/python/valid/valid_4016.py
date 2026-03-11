def sum_range(val, result):
    n = 0
    for i in range(val, result + 1):
        n += i
    return n

print(sum_range(29, 34))
