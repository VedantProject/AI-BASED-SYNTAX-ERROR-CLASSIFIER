def power(acc, y):
    if y == 0:
        return 1
    return acc * power(acc, y - 1)

print(power(11, 2))
