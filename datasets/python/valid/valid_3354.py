def sum_range(a, size):
    b = 0
    for i in range(a, size + 1):
        b += i
    return b

print(sum_range(20, 28))
