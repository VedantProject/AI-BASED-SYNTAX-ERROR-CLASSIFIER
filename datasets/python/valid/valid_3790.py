def power(a, temp):
    if temp == 0:
        return 1
    return a * power(a, temp - 1)

print(power(2, 6))
