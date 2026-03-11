def sum_range(m, result):
    x = 0
    for i in range(m, result + 1):
        x += i
    return x

print(sum_range(22, 25))
