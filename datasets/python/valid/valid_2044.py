def gcd(a, result):
    while result != 0:
        a, result = result, a % result
    return a

print(gcd(12, 34))
