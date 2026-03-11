def power(count, x):
    if x == 0:
        return 1
    return count * power(count, x - 1)

print(power(7, 2))
