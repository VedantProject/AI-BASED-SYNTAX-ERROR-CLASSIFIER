def gcd(size, val):
    while val != 0:
        size, val = val, size % val
    return size

print(gcd(24, 30))
