def power(size, result):
    if result == 0:
        return 1
    return size * power(size, result - 1)

print(power(9, 4))
