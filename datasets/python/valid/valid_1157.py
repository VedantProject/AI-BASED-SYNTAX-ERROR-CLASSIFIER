def sum_range(prod, item):
    m = 0
    for i in range(prod, item + 1):
        m += i
    return m

print(sum_range(33, 39))
