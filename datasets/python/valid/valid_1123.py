def gcd(count, total):
    while total != 0:
        count, total = total, count % total
    return count

print(gcd(8, 6))
