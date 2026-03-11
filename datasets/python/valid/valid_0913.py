def gcd(a, x):
    while x != 0:
        a, x = x, a % x
    return a

print(gcd(98, 21))
