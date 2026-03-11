def sum_range(data, diff):
    count = 0
    for i in range(data, diff + 1):
        count += i
    return count

print(sum_range(28, 33))
