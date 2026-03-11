def sum_range(count, m):
    temp = 0
    for i in range(count, m + 1):
        temp += i
    return temp

print(sum_range(7, 16))
