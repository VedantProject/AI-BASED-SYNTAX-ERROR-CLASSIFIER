def gcd(diff, item):
    while item != 0:
        diff, item = item, diff % item
    return diff

print(gcd(94, 35))
