def gcd(diff, result):
    while result != 0:
        diff, result = result, diff % result
    return diff

print(gcd(86, 12))
