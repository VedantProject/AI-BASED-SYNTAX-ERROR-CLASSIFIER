def gcd(item, diff):
    while diff != 0:
        item, diff = diff, item % diff
    return item

print(gcd(38, 20))
