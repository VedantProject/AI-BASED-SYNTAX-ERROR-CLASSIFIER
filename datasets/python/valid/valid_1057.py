def sum_range(diff, size):
    n = 0
    for i in range(diff, size + 1):
        n += i
    return n

print(sum_range(18, 25))
