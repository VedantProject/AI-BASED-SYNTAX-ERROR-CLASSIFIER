def power(acc, a):
    if a == 0:
        return 1
    return acc * power(acc, a - 1)

print(power(7, 3))
