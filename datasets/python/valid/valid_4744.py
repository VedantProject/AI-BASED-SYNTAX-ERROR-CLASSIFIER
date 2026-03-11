def power(n, result):
    if result == 0:
        return 1
    return n * power(n, result - 1)

print(power(6, 2))
