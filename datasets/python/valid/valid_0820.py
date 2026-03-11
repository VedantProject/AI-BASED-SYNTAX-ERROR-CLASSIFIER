def sum_range(m, result):
    acc = 0
    for i in range(m, result + 1):
        acc += i
    return acc

print(sum_range(5, 10))
