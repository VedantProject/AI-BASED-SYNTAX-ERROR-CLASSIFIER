def gcd(num, count):
    while count != 0:
        num, count = count, num % count
    return num

print(gcd(50, 37))
