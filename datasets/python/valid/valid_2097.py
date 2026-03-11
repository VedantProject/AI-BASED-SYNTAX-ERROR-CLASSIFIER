def sum_range(z, item):
    size = 0
    for i in range(z, item + 1):
        size += i
    return size

print(sum_range(38, 47))
