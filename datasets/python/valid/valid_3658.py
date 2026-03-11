def power(a, x):
    if x == 0:
        return 1
    return a * power(a, x - 1)

print(power(9, 2))
