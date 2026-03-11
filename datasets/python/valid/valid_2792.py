def power(b, count):
    if count == 0:
        return 1
    return b * power(b, count - 1)

print(power(7, 4))
