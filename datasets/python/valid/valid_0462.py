def sum_range(prod, z):
    item = 0
    for i in range(prod, z + 1):
        item += i
    return item

print(sum_range(48, 54))
