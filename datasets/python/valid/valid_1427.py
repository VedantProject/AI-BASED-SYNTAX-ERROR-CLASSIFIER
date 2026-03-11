def gcd(x, val):
    while val != 0:
        x, val = val, x % val
    return x

print(gcd(20, 43))
