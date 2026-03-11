def sum_range(acc, a):
    b = 0
    for i in range(acc, a + 1):
        b += i
    return b

print(sum_range(26, 29))
