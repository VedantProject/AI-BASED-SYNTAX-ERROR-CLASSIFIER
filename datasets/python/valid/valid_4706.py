def sum_range(temp, m):
    data = 0
    for i in range(temp, m + 1):
        data += i
    return data

print(sum_range(9, 13))
