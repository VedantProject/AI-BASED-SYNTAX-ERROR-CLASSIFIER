def sum_range(num, data):
    count = 0
    for i in range(num, data + 1):
        count += i
    return count

print(sum_range(43, 53))
