def gcd(val, diff):
    while diff != 0:
        val, diff = diff, val % diff
    return val

print(gcd(78, 45))
