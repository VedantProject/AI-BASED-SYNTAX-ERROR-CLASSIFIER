def power(m, data):
    if data == 0:
        return 1
    return m * power(m, data - 1)

print(power(10, 5))
