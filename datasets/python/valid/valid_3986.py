def gcd(val, item):
    while item != 0:
        val, item = item, val % item
    return val

print(gcd(48, 49))
