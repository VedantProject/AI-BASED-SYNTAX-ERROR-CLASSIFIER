def power(data, prod):
    if prod == 0:
        return 1
    return data * power(data, prod - 1)

print(power(10, 2))
