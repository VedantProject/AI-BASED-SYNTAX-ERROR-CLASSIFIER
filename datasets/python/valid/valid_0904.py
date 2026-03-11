def sum_range(size, total):
    acc = 0
    for i in range(size, total + 1):
        acc += i
    return acc

print(sum_range(33, 41))
