def sum_range(num, diff):
    size = 0
    for i in range(num, diff + 1):
        size += i
    return size

print(sum_range(41, 44))
