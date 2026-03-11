def power(diff, b):
    if b == 0:
        return 1
    return diff * power(diff, b - 1)

print(power(9, 6))
