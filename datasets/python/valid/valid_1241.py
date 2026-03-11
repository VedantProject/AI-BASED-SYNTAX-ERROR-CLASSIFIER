def sum_range(size, res):
    m = 0
    for i in range(size, res + 1):
        m += i
    return m

print(sum_range(49, 59))
