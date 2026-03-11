def gcd(prod, acc):
    while acc != 0:
        prod, acc = acc, prod % acc
    return prod

print(gcd(26, 34))
