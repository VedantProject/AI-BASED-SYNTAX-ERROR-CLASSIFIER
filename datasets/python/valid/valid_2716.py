def power(x, res):
    if res == 0:
        return 1
    return x * power(x, res - 1)

print(power(2, 2))
