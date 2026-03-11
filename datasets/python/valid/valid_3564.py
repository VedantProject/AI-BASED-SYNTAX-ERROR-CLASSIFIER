def power(prod, m):
    if m == 0:
        return 1
    return prod * power(prod, m - 1)

print(power(9, 4))
