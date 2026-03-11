def sum_range(m, result):
    n = 0
    for i in range(m, result + 1):
        n += i
    return n

print(sum_range(23, 28))
