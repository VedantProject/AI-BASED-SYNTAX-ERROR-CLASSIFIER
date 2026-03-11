def sum_range(data, count):
    x = 0
    for i in range(data, count + 1):
        x += i
    return x

print(sum_range(41, 44))
