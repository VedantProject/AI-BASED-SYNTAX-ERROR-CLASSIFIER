def gcd(total, a):
    while a != 0:
        total, a = a, total % a
    return total

print(gcd(4, 7))
