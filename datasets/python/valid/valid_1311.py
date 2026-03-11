def gcd(b, result):
    while result != 0:
        b, result = result, b % result
    return b

print(gcd(100, 48))
