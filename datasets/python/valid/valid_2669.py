def sum_range(count, data):
    temp = 0
    for i in range(count, data + 1):
        temp += i
    return temp

print(sum_range(43, 52))
