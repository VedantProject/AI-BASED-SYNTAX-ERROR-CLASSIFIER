def gcd(a, z):
    while z != 0:
        a, z = z, a % z
    return a

print(gcd(20, 35))
