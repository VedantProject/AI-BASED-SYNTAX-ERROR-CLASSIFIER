def gcd(val, y):
    while y != 0:
        val, y = y, val % y
    return val

print(gcd(52, 18))
