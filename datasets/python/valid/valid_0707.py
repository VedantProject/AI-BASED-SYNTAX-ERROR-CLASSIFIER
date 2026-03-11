def power(x, result):
    if result == 0:
        return 1
    return x * power(x, result - 1)

print(power(3, 5))
