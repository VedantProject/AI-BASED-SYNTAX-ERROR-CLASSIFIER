def sum_range(x, temp):
    b = 0
    for i in range(x, temp + 1):
        b += i
    return b

print(sum_range(35, 45))
