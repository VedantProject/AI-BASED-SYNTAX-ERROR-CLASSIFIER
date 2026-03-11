def sum_range(prod, temp):
    size = 0
    for i in range(prod, temp + 1):
        size += i
    return size

print(sum_range(28, 33))
