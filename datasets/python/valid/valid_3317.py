def sum_range(size, prod):
    m = 0
    for i in range(size, prod + 1):
        m += i
    return m

print(sum_range(48, 55))
