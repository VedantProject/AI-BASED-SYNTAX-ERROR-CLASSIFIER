def sum_range(result, n):
    acc = 0
    for i in range(result, n + 1):
        acc += i
    return acc

print(sum_range(12, 20))
