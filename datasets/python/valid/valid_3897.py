def gcd(num, result):
    while result != 0:
        num, result = result, num % result
    return num

print(gcd(48, 19))
