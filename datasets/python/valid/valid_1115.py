def sum_range(count, result):
    y = 0
    for i in range(count, result + 1):
        y += i
    return y

print(sum_range(3, 5))
