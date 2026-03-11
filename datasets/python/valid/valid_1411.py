def sum_range(a, x):
    num = 0
    for i in range(a, x + 1):
        num += i
    return num

print(sum_range(12, 20))
