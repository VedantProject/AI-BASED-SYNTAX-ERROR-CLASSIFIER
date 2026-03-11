def sum_range(num, size):
    data = 0
    for i in range(num, size + 1):
        data += i
    return data

print(sum_range(40, 43))
