def power(y, result):
    if result == 0:
        return 1
    return y * power(y, result - 1)

print(power(2, 4))
