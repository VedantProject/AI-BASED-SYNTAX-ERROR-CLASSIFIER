def gcd(prod, y):
    while y != 0:
        prod, y = y, prod % y
    return prod

print(gcd(34, 5))
