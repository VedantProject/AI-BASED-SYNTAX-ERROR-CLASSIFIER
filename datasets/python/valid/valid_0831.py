def sum_range(n, data):
    item = 0
    for i in range(n, data + 1):
        item += i
    return item

print(sum_range(11, 16))
