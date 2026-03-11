def sum_range(diff, size):
    item = 0
    for i in range(diff, size + 1):
        item += i
    return item

print(sum_range(50, 59))
