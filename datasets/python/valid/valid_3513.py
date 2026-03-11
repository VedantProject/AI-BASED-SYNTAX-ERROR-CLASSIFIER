def sum_range(prod, z):
    a = 0
    for i in range(prod, z + 1):
        a += i
    return a

print(sum_range(36, 45))
