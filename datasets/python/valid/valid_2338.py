def gcd(acc, diff):
    while diff != 0:
        acc, diff = diff, acc % diff
    return acc

print(gcd(92, 48))
