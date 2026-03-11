def gcd(b, count):
    while count != 0:
        b, count = count, b % count
    return b

print(gcd(92, 7))
