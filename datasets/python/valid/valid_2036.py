def power(y, prod):
    if prod == 0:
        return 1
    return y * power(y, prod - 1)

print(power(5, 5))
