def gcd(temp, z):
    while z != 0:
        temp, z = z, temp % z
    return temp

print(gcd(46, 30))
