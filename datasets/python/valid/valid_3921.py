def sum_range(y, acc):
    b = 0
    for i in range(y, acc + 1):
        b += i
    return b

print(sum_range(11, 19))
