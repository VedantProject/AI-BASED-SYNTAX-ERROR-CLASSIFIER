def sum_range(z, res):
    y = 0
    for i in range(z, res + 1):
        y += i
    return y

print(sum_range(42, 49))
