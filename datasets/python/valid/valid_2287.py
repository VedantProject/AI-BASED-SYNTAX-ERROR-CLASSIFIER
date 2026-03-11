def power(b, n):
    if n == 0:
        return 1
    return b * power(b, n - 1)

print(power(6, 5))
