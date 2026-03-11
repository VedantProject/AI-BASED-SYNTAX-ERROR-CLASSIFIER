def sum_range(count, n):
    data = 0
    for i in range(count, n + 1):
        data += i
    return data

print(sum_range(25, 34))
