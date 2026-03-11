def sum_range(acc, temp):
    m = 0
    for i in range(acc, temp + 1):
        m += i
    return m

print(sum_range(25, 35))
