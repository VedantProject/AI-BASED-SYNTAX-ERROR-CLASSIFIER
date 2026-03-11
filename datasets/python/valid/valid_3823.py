def gcd(x, z):
    while z != 0:
        x, z = z, x % z
    return x

print(gcd(32, 28))
