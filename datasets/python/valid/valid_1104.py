def sum_range(count, total):
    result = 0
    for i in range(count, total + 1):
        result += i
    return result

print(sum_range(18, 25))
