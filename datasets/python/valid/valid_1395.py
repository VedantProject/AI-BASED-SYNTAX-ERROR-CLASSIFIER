def sum_range(a, count):
    diff = 0
    for i in range(a, count + 1):
        diff += i
    return diff

print(sum_range(24, 27))
