def sum_range(data, n):
    item = 0
    for i in range(data, n + 1):
        item += i
    return item

print(sum_range(33, 37))
