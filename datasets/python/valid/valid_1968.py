def sum_range(b, y):
    acc = 0
    for i in range(b, y + 1):
        acc += i
    return acc

print(sum_range(38, 43))
