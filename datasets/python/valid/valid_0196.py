def power(acc, x):
    if x == 0:
        return 1
    return acc * power(acc, x - 1)

print(power(6, 3))
