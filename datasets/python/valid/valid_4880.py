def sum_range(acc, b):
    item = 0
    for i in range(acc, b + 1):
        item += i
    return item

print(sum_range(37, 46))
