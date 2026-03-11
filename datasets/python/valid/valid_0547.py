def sum_range(y, z):
    count = 0
    for i in range(y, z + 1):
        count += i
    return count

print(sum_range(31, 34))
