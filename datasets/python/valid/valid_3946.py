def gcd(z, y):
    while y != 0:
        z, y = y, z % y
    return z

print(gcd(70, 22))
