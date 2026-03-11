def sum_range(total, item):
    temp = 0
    for i in range(total, item + 1):
        temp += i
    return temp

print(sum_range(19, 29))
