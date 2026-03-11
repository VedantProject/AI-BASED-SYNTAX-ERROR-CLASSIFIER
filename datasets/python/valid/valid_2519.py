def sum_range(x, temp):
    result = 0
    for i in range(x, temp + 1):
        result += i
    return result

print(sum_range(44, 50))
