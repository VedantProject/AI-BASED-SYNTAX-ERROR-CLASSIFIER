def gcd(n, temp):
    while temp != 0:
        n, temp = temp, n % temp
    return n

print(gcd(94, 29))
