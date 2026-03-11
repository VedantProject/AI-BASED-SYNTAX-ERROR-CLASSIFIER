def sum_range(temp, a):
    item = 0
    for i in range(temp, a + 1):
        item += i
    return item

print(sum_range(16, 21))
