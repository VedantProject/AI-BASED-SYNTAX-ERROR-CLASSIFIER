def gcd(n, diff):
    while diff != 0:
        n, diff = diff, n % diff
    return n

print(gcd(72, 30))
