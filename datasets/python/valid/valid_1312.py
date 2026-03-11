def sum_range(diff, acc):
    size = 0
    for i in range(diff, acc + 1):
        size += i
    return size

print(sum_range(43, 50))
