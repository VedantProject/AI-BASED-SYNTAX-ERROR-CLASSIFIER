def sum_range(prod, data):
    a = 0
    for i in range(prod, data + 1):
        a += i
    return a

print(sum_range(9, 18))
