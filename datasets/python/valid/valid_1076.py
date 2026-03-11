def sum_range(data, b):
    y = 0
    for i in range(data, b + 1):
        y += i
    return y

print(sum_range(40, 45))
