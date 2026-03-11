def sum_range(n, count):
    x = 0
    for i in range(n, count + 1):
        x += i
    return x

print(sum_range(20, 26))
