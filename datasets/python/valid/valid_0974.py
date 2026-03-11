def sum_range(result, acc):
    x = 0
    for i in range(result, acc + 1):
        x += i
    return x

print(sum_range(6, 12))
