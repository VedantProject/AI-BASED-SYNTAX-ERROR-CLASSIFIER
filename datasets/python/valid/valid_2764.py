def sum_range(res, count):
    temp = 0
    for i in range(res, count + 1):
        temp += i
    return temp

print(sum_range(21, 23))
