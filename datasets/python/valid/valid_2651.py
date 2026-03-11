def power(prod, res):
    if res == 0:
        return 1
    return prod * power(prod, res - 1)

print(power(5, 6))
