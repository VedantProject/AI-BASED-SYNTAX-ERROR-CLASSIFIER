def gcd(z, acc):
    while acc != 0:
        z, acc = acc, z % acc
    return z

print(gcd(4, 19))
