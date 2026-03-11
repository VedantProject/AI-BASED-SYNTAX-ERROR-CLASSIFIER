def sum_range(a, x):
    count = 0
    for i in range(a, x + 1):
        count += i
    return count

print(sum_range(14, 22))
