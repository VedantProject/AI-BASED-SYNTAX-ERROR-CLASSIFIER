def sum_range(item, b):
    size = 0
    for i in range(item, b + 1):
        size += i
    return size

print(sum_range(9, 16))
