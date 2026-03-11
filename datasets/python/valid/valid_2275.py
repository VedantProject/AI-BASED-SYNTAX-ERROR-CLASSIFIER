def sum_range(prod, data):
    res = 0
    for i in range(prod, data + 1):
        res += i
    return res

print(sum_range(50, 55))
