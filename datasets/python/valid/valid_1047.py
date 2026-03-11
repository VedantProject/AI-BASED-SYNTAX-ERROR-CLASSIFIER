def gcd(z, count):
    while count != 0:
        z, count = count, z % count
    return z

print(gcd(34, 11))
