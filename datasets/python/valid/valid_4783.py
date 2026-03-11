def gcd(b, x):
    while x != 0:
        b, x = x, b % x
    return b

print(gcd(88, 16))
