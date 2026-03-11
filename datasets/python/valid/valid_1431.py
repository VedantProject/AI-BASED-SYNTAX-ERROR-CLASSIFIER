def power(acc, n):
    if n == 0:
        return 1
    return acc * power(acc, n - 1)

print(power(10, 2))
