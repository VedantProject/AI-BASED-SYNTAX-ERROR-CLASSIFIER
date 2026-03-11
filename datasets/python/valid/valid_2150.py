def sum_range(item, diff):
    result = 0
    for i in range(item, diff + 1):
        result += i
    return result

print(sum_range(8, 12))
