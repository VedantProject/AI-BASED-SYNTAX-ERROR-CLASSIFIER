def sum_range(z, acc):
    count = 0
    for i in range(z, acc + 1):
        count += i
    return count

print(sum_range(43, 53))
