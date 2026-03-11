def sum_range(result, a):
    item = 0
    for i in range(result, a + 1):
        item += i
    return item

print(sum_range(33, 39))
