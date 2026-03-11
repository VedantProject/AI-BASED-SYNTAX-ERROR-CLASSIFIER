def sum_range(m, size):
    temp = 0
    for i in range(m, size + 1):
        temp += i
    return temp

print(sum_range(20, 26))
