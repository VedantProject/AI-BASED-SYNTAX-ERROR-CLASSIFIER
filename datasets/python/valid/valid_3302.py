def gcd(z, diff):
    while diff != 0:
        z, diff = diff, z % diff
    return z

print(gcd(64, 9))
