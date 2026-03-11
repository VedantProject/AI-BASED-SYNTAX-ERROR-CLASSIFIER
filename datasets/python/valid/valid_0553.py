def sum_range(res, x):
    num = 0
    for i in range(res, x + 1):
        num += i
    return num

print(sum_range(44, 53))
