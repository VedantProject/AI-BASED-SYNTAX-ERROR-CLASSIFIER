def gcd(diff, z):
    while z != 0:
        diff, z = z, diff % z
    return diff

print(gcd(38, 35))
