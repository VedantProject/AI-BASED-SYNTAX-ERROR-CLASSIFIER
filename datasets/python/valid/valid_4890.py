def power(data, a):
    if a == 0:
        return 1
    return data * power(data, a - 1)

print(power(5, 2))
