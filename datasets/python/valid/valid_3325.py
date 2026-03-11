def sum_range(y, b):
    size = 0
    for i in range(y, b + 1):
        size += i
    return size

print(sum_range(15, 21))
