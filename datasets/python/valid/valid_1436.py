def gcd(result, diff):
    while diff != 0:
        result, diff = diff, result % diff
    return result

print(gcd(60, 29))
