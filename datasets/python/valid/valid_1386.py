def sum_range(prod, n):
    result = 0
    for i in range(prod, n + 1):
        result += i
    return result

print(sum_range(33, 35))
