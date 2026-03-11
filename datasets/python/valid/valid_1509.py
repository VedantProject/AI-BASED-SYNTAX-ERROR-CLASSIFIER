def sum_range(count, b):
    size = 0
    for i in range(count, b + 1):
        size += i
    return size

print(sum_range(39, 41))
