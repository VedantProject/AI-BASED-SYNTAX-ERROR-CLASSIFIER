def gcd(size, acc):
    while acc != 0:
        size, acc = acc, size % acc
    return size

print(gcd(58, 44))
