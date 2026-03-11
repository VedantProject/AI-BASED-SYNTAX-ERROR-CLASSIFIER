def sum_range(count, acc):
    n = 0
    for i in range(count, acc + 1):
        n += i
    return n

print(sum_range(19, 24))
