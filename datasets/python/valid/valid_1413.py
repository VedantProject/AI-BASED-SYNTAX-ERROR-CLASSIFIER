def sum_range(num, res):
    a = 0
    for i in range(num, res + 1):
        a += i
    return a

print(sum_range(43, 53))
