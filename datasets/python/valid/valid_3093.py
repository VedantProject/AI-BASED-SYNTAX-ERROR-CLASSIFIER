def sum_range(prod, temp):
    x = 0
    for i in range(prod, temp + 1):
        x += i
    return x

print(sum_range(23, 31))
