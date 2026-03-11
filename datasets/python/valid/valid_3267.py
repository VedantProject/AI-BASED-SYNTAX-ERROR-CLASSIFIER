def gcd(diff, val):
    while val != 0:
        diff, val = val, diff % val
    return diff

print(gcd(44, 27))
