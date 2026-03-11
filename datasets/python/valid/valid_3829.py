def gcd(acc, b):
    while b != 0:
        acc, b = b, acc % b
    return acc

print(gcd(40, 4))
