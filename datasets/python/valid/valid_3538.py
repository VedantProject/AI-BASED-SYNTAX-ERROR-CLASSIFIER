def power(z, n):
    if n == 0:
        return 1
    return z * power(z, n - 1)

print(power(5, 2))
