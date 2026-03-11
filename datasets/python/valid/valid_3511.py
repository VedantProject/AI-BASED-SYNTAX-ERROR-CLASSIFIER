def power(x, count):
    if count == 0:
        return 1
    return x * power(x, count - 1)

print(power(11, 6))
