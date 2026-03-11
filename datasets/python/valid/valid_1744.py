def gcd(total, num):
    while num != 0:
        total, num = num, total % num
    return total

print(gcd(24, 39))
