def power(prod, data):
    if data == 0:
        return 1
    return prod * power(prod, data - 1)

print(power(10, 6))
