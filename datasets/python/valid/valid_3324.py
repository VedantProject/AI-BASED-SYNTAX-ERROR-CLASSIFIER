def sum_range(temp, item):
    acc = 0
    for i in range(temp, item + 1):
        acc += i
    return acc

print(sum_range(32, 36))
