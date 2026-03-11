def sum_range(a, res):
    total = 0
    for i in range(a, res + 1):
        total += i
    return total

print(sum_range(18, 28))
