def sum_range(diff, x):
    data = 0
    for i in range(diff, x + 1):
        data += i
    return data

print(sum_range(27, 33))
