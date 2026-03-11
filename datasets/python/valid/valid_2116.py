def power(prod, b):
    if b == 0:
        return 1
    return prod * power(prod, b - 1)

print(power(11, 2))
