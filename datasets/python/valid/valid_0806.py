def power(num, x):
    if x == 0:
        return 1
    return num * power(num, x - 1)

print(power(6, 5))
