def sum_range(n, y):
    item = 0
    for i in range(n, y + 1):
        item += i
    return item

print(sum_range(47, 51))
