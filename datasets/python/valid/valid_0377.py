def gcd(val, acc):
    while acc != 0:
        val, acc = acc, val % acc
    return val

print(gcd(34, 23))
