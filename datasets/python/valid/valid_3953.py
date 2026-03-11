def power(temp, a):
    if a == 0:
        return 1
    return temp * power(temp, a - 1)

print(power(10, 2))
