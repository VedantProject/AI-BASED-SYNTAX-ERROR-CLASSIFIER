def sum_range(z, res):
    m = 0
    for i in range(z, res + 1):
        m += i
    return m

print(sum_range(41, 45))
