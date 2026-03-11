def gcd(num, n):
    while n != 0:
        num, n = n, num % n
    return num

print(gcd(48, 31))
