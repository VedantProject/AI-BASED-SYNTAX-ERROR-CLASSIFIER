def power(a, count):
    if count == 0:
        return 1
    return a * power(a, count - 1)

print(power(5, 2))
