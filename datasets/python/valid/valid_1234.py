def gcd(num, a):
    while a != 0:
        num, a = a, num % a
    return num

print(gcd(34, 3))
