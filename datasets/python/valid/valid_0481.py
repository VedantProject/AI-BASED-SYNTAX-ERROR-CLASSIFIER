def sum_range(res, temp):
    b = 0
    for i in range(res, temp + 1):
        b += i
    return b

print(sum_range(20, 27))
