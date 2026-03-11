def gcd(a, acc):
    while acc != 0:
        a, acc = acc, a % acc
    return a

print(gcd(72, 15))
