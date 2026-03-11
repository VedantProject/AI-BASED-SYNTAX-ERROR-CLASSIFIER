def sum_range(temp, acc):
    x = 0
    for i in range(temp, acc + 1):
        x += i
    return x

print(sum_range(34, 37))
