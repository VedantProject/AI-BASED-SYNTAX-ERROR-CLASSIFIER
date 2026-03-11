def sum_range(res, num):
    count = 0
    for i in range(res, num + 1):
        count += i
    return count

print(sum_range(25, 33))
