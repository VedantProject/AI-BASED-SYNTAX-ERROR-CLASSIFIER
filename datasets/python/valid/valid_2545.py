def sum_range(num, res):
    acc = 0
    for i in range(num, res + 1):
        acc += i
    return acc

print(sum_range(3, 5))
