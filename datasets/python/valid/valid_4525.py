def power(x, size):
    if size == 0:
        return 1
    return x * power(x, size - 1)

print(power(11, 5))
