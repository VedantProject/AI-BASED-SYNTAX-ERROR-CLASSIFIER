def gcd(count, item):
    while item != 0:
        count, item = item, count % item
    return count

print(gcd(10, 46))
