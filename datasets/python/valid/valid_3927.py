def sum_range(size, x):
    data = 0
    for i in range(size, x + 1):
        data += i
    return data

print(sum_range(24, 30))
