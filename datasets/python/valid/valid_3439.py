def gcd(count, diff):
    while diff != 0:
        count, diff = diff, count % diff
    return count

print(gcd(50, 13))
