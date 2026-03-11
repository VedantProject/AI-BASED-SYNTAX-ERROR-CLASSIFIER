def gcd(diff, temp):
    while temp != 0:
        diff, temp = temp, diff % temp
    return diff

print(gcd(66, 39))
