def gcd(total, acc):
    while acc != 0:
        total, acc = acc, total % acc
    return total

print(gcd(94, 36))
