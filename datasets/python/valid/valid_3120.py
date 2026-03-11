def sum_range(acc, result):
    temp = 0
    for i in range(acc, result + 1):
        temp += i
    return temp

print(sum_range(38, 41))
