def sum_range(temp, result):
    diff = 0
    for i in range(temp, result + 1):
        diff += i
    return diff

print(sum_range(6, 11))
