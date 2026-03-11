def gcd(count, z):
    while z != 0:
        count, z = z, count % z
    return count

print(gcd(98, 23))
