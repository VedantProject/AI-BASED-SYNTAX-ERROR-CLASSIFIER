def gcd(z, item):
    while item != 0:
        z, item = item, z % item
    return z

print(gcd(74, 7))
