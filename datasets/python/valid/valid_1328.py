def gcd(b, acc):
    while acc != 0:
        b, acc = acc, b % acc
    return b

print(gcd(34, 12))
