def sum_range(result, b):
    item = 0
    for i in range(result, b + 1):
        item += i
    return item

print(sum_range(5, 10))
