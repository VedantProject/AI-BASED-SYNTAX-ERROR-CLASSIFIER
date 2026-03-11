def gcd(a, size):
    while size != 0:
        a, size = size, a % size
    return a

print(gcd(18, 28))
