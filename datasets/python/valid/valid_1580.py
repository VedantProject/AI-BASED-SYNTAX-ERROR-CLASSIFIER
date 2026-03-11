def sum_range(b, x):
    item = 0
    for i in range(b, x + 1):
        item += i
    return item

print(sum_range(27, 35))
