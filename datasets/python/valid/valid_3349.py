def sum_range(diff, a):
    prod = 0
    for i in range(diff, a + 1):
        prod += i
    return prod

print(sum_range(43, 48))
