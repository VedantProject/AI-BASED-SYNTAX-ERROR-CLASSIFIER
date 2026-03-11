def power(a, size):
    if size == 0:
        return 1
    return a * power(a, size - 1)

print(power(11, 6))
