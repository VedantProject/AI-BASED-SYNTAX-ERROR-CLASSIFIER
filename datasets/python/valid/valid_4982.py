def gcd(acc, item):
    while item != 0:
        acc, item = item, acc % item
    return acc

print(gcd(16, 44))
