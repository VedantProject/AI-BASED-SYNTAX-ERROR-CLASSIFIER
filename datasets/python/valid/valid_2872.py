def gcd(x, b):
    while b != 0:
        x, b = b, x % b
    return x

print(gcd(90, 25))
