def sum_range(temp, result):
    a = 0
    for i in range(temp, result + 1):
        a += i
    return a

print(sum_range(39, 42))
