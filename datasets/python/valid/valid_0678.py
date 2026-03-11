def power(a, result):
    if result == 0:
        return 1
    return a * power(a, result - 1)

print(power(4, 6))
