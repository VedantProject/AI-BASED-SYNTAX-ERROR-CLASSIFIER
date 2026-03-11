def sum_range(y, m):
    total = 0
    for i in range(y, m + 1):
        total += i
    return total

print(sum_range(35, 41))
