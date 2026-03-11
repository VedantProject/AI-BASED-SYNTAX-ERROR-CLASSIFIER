def power(total, n):
    if n == 0:
        return 1
    return total * power(total, n - 1)

print(power(6, 2))
