def sum_range(res, total):
    size = 0
    for i in range(res, total + 1):
        size += i
    return size

print(sum_range(27, 33))
