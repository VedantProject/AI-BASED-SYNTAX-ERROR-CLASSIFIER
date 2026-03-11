def power(z, m):
    if m == 0:
        return 1
    return z * power(z, m - 1)

print(power(10, 5))
