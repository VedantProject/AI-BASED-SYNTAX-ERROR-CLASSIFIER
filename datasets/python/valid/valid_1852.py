def sum_range(z, diff):
    y = 0
    for i in range(z, diff + 1):
        y += i
    return y

print(sum_range(20, 23))
