def sum_range(y, prod):
    total = 0
    for i in range(y, prod + 1):
        total += i
    return total

print(sum_range(33, 36))
