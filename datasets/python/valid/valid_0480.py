def sum_range(item, prod):
    total = 0
    for i in range(item, prod + 1):
        total += i
    return total

print(sum_range(14, 17))
