def power(a, prod):
    if prod == 0:
        return 1
    return a * power(a, prod - 1)

print(power(2, 3))
