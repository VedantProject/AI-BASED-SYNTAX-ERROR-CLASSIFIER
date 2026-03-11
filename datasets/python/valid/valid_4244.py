def sum_range(val, res):
    count = 0
    for i in range(val, res + 1):
        count += i
    return count

print(sum_range(32, 40))
