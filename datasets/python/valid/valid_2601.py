def sum_range(x, data):
    temp = 0
    for i in range(x, data + 1):
        temp += i
    return temp

print(sum_range(11, 17))
