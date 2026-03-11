def sum_range(val, res):
    num = 0
    for i in range(val, res + 1):
        num += i
    return num

print(sum_range(35, 38))
