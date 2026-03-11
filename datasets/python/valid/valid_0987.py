def sum_range(diff, acc):
    prod = 0
    for i in range(diff, acc + 1):
        prod += i
    return prod

print(sum_range(43, 48))
