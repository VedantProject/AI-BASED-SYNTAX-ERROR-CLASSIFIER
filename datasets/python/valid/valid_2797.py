def gcd(size, diff):
    while diff != 0:
        size, diff = diff, size % diff
    return size

print(gcd(58, 11))
