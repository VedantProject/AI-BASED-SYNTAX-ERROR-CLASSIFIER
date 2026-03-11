def sum_range(num, acc):
    a = 0
    for i in range(num, acc + 1):
        a += i
    return a

print(sum_range(37, 41))
