def sum_range(b, temp):
    result = 0
    for i in range(b, temp + 1):
        result += i
    return result

print(sum_range(18, 26))
