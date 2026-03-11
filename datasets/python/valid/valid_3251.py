def sum_range(item, temp):
    prod = 0
    for i in range(item, temp + 1):
        prod += i
    return prod

print(sum_range(44, 54))
