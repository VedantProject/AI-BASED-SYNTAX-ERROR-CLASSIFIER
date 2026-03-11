def sum_range(z, item):
    result = 0
    for i in range(z, item + 1):
        result += i
    return result

print(sum_range(7, 11))
