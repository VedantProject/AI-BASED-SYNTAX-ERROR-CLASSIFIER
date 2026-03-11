def sum_range(temp, data):
    num = 0
    for i in range(temp, data + 1):
        num += i
    return num

print(sum_range(34, 43))
