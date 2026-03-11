def gcd(x, a):
    while a != 0:
        x, a = a, x % a
    return x

print(gcd(22, 30))
