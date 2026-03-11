def sum_range(count, diff):
    data = 0
    for i in range(count, diff + 1):
        data += i
    return data

print(sum_range(3, 10))
