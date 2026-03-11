def sum_range(b, data):
    num = 0
    for i in range(b, data + 1):
        num += i
    return num

print(sum_range(25, 35))
