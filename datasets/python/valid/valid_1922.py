def gcd(y, z):
    while z != 0:
        y, z = z, y % z
    return y

print(gcd(80, 10))
