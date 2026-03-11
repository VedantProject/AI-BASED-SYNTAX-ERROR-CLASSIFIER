def sum_range(count, n):
    result = 0
    for i in range(count, n + 1):
        result += i
    return result

print(sum_range(34, 36))
