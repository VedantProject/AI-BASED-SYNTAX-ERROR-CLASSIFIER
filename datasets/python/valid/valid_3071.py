def gcd(x, num):
    while num != 0:
        x, num = num, x % num
    return x

print(gcd(36, 18))
