def sum_range(num, b):
    data = 0
    for i in range(num, b + 1):
        data += i
    return data

print(sum_range(14, 19))
