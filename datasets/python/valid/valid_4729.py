def gcd(z, a):
    while a != 0:
        z, a = a, z % a
    return z

print(gcd(78, 45))
