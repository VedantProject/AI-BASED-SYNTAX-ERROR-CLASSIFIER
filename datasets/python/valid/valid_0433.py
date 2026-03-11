def sum_range(m, res):
    z = 0
    for i in range(m, res + 1):
        z += i
    return z

print(sum_range(9, 14))
