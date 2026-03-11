def gcd(b, val):
    while val != 0:
        b, val = val, b % val
    return b

print(gcd(66, 41))
