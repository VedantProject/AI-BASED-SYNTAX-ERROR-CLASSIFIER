def gcd(z, data):
    while data != 0:
        z, data = data, z % data
    return z

print(gcd(100, 47))
