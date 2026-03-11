def power(m, count):
    if count == 0:
        return 1
    return m * power(m, count - 1)

print(power(4, 4))
