def sum_range(z, x):
    num = 0
    for i in range(z, x + 1):
        num += i
    return num

print(sum_range(32, 42))
