def sum_range(data, res):
    size = 0
    for i in range(data, res + 1):
        size += i
    return size

print(sum_range(38, 44))
