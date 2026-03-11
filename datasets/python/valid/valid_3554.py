def sum_range(result, a):
    count = 0
    for i in range(result, a + 1):
        count += i
    return count

print(sum_range(27, 37))
