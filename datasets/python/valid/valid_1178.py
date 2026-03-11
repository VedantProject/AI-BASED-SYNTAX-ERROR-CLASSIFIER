def sum_range(size, res):
    result = 0
    for i in range(size, res + 1):
        result += i
    return result

print(sum_range(32, 36))
