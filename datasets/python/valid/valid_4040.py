def gcd(z, result):
    while result != 0:
        z, result = result, z % result
    return z

print(gcd(22, 43))
