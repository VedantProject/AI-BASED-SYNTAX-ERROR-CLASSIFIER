def sum_range(m, x):
    result = 0
    for i in range(m, x + 1):
        result += i
    return result

print(sum_range(15, 25))
