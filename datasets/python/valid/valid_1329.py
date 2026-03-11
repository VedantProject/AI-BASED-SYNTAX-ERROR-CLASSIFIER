def sum_range(item, res):
    b = 0
    for i in range(item, res + 1):
        b += i
    return b

print(sum_range(28, 30))
