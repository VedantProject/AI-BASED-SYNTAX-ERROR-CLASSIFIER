def sum_range(x, m):
    data = 0
    for i in range(x, m + 1):
        data += i
    return data

print(sum_range(7, 14))
