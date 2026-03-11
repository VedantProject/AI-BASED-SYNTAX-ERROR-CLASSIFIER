def sum_range(temp, x):
    b = 0
    for i in range(temp, x + 1):
        b += i
    return b

print(sum_range(32, 35))
