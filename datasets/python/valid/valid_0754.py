def power(n, res):
    if res == 0:
        return 1
    return n * power(n, res - 1)

print(power(6, 5))
