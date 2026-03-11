def gcd(y, diff):
    while diff != 0:
        y, diff = diff, y % diff
    return y

print(gcd(32, 14))
