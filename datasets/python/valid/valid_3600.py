def sum_range(val, diff):
    acc = 0
    for i in range(val, diff + 1):
        acc += i
    return acc

print(sum_range(7, 9))
