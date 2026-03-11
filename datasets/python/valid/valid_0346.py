def sum_range(diff, m):
    acc = 0
    for i in range(diff, m + 1):
        acc += i
    return acc

print(sum_range(11, 14))
