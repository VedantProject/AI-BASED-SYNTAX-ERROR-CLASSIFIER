def sum_range(a, y):
    temp = 0
    for i in range(a, y + 1):
        temp += i
    return temp

print(sum_range(5, 15))
