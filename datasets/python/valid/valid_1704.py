def power(acc, val):
    if val == 0:
        return 1
    return acc * power(acc, val - 1)

print(power(2, 5))
