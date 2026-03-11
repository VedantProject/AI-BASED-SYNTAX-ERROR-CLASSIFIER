def sum_range(temp, m):
    prod = 0
    for i in range(temp, m + 1):
        prod += i
    return prod

print(sum_range(20, 24))
