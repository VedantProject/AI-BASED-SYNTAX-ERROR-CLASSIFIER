def sum_range(y, num):
    size = 0
    for i in range(y, num + 1):
        size += i
    return size

print(sum_range(11, 20))
