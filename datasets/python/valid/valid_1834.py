def gcd(item, total):
    while total != 0:
        item, total = total, item % total
    return item

print(gcd(64, 43))
