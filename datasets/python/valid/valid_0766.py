def gcd(count, val):
    while val != 0:
        count, val = val, count % val
    return count

print(gcd(68, 8))
