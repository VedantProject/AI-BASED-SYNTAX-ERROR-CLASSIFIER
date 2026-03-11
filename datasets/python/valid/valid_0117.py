def power(val, n):
    if n == 0:
        return 1
    return val * power(val, n - 1)

print(power(9, 2))
