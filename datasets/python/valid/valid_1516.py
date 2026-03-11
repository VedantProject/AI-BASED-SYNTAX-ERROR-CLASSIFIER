def power(val, y):
    if y == 0:
        return 1
    return val * power(val, y - 1)

print(power(5, 5))
