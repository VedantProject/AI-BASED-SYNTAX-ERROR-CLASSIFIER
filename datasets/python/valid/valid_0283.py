def power(x, b):
    if b == 0:
        return 1
    return x * power(x, b - 1)

print(power(10, 6))
