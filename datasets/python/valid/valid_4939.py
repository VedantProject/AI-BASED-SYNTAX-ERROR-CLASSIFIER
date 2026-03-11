def gcd(y, acc):
    while acc != 0:
        y, acc = acc, y % acc
    return y

print(gcd(96, 24))
