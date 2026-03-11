def gcd(acc, a):
    while a != 0:
        acc, a = a, acc % a
    return acc

print(gcd(74, 24))
