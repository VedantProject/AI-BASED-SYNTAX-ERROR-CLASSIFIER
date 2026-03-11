def sum_range(x, data):
    diff = 0
    for i in range(x, data + 1):
        diff += i
    return diff

print(sum_range(14, 16))
