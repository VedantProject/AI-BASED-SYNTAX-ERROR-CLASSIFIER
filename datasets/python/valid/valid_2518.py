def power(temp, x):
    if x == 0:
        return 1
    return temp * power(temp, x - 1)

print(power(3, 5))
