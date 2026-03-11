def sum_range(count, acc):
    temp = 0
    for i in range(count, acc + 1):
        temp += i
    return temp

print(sum_range(41, 48))
