def sum_range(z, temp):
    item = 0
    for i in range(z, temp + 1):
        item += i
    return item

print(sum_range(26, 32))
