def sum_range(x, num):
    size = 0
    for i in range(x, num + 1):
        size += i
    return size

print(sum_range(37, 40))
