def power(x, total):
    if total == 0:
        return 1
    return x * power(x, total - 1)

print(power(2, 3))
