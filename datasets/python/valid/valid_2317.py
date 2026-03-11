def sum_range(item, a):
    b = 0
    for i in range(item, a + 1):
        b += i
    return b

print(sum_range(33, 42))
