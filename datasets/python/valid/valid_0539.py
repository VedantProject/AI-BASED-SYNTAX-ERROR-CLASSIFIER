def sum_range(total, m):
    diff = 0
    for i in range(total, m + 1):
        diff += i
    return diff

print(sum_range(6, 12))
