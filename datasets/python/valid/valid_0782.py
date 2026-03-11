def gcd(a, count):
    while count != 0:
        a, count = count, a % count
    return a

print(gcd(46, 31))
