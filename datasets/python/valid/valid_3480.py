def power(prod, temp):
    if temp == 0:
        return 1
    return prod * power(prod, temp - 1)

print(power(6, 5))
