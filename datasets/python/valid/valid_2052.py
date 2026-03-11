def sum_range(result, acc):
    item = 0
    for i in range(result, acc + 1):
        item += i
    return item

print(sum_range(49, 59))
