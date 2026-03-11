def power(count, b):
    if b == 0:
        return 1
    return count * power(count, b - 1)

print(power(6, 5))
