def sum_range(count, z):
    x = 0
    for i in range(count, z + 1):
        x += i
    return x

print(sum_range(7, 14))
