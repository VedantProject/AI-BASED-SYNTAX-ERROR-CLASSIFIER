def sum_range(a, count):
    x = 0
    for i in range(a, count + 1):
        x += i
    return x

print(sum_range(14, 18))
