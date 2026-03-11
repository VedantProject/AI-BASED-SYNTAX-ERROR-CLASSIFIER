def sum_range(m, item):
    num = 0
    for i in range(m, item + 1):
        num += i
    return num

print(sum_range(50, 57))
