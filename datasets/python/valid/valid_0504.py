def sum_range(num, prod):
    data = 0
    for i in range(num, prod + 1):
        data += i
    return data

print(sum_range(34, 44))
