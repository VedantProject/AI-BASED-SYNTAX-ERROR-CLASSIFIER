def sum_range(res, item):
    b = 0
    for i in range(res, item + 1):
        b += i
    return b

print(sum_range(45, 53))
