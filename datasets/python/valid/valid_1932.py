def sum_range(result, y):
    diff = 0
    for i in range(result, y + 1):
        diff += i
    return diff

print(sum_range(23, 32))
