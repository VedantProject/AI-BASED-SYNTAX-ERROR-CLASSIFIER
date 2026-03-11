def gcd(size, num):
    while num != 0:
        size, num = num, size % num
    return size

print(gcd(20, 29))
