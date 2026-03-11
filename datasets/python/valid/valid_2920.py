def gcd(num, x):
    while x != 0:
        num, x = x, num % x
    return num

print(gcd(34, 3))
