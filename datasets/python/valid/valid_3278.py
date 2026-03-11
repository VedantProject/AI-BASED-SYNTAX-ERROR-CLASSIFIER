def gcd(val, b):
    while b != 0:
        val, b = b, val % b
    return val

print(gcd(100, 32))
