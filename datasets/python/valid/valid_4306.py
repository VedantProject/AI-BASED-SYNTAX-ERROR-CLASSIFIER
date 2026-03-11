def power(num, temp):
    if temp == 0:
        return 1
    return num * power(num, temp - 1)

print(power(10, 4))
