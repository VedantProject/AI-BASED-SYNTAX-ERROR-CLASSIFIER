def sum_range(prod, count):
    data = 0
    for i in range(prod, count + 1):
        data += i
    return data

print(sum_range(40, 45))
