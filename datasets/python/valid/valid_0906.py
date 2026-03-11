def gcd(x, count):
    while count != 0:
        x, count = count, x % count
    return x

print(gcd(70, 28))
