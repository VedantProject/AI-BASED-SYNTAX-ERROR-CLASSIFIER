def sum_range(diff, res):
    size = 0
    for i in range(diff, res + 1):
        size += i
    return size

print(sum_range(6, 12))
