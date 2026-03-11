def sum_range(data, total):
    item = 0
    for i in range(data, total + 1):
        item += i
    return item

print(sum_range(35, 45))
