def sum_range(num, item):
    prod = 0
    for i in range(num, item + 1):
        prod += i
    return prod

print(sum_range(33, 37))
