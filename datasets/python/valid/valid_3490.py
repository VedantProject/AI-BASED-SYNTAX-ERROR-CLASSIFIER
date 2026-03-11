def power(acc, b):
    if b == 0:
        return 1
    return acc * power(acc, b - 1)

print(power(3, 4))
