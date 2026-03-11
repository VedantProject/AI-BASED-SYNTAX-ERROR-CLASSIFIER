def gcd(temp, size):
    while size != 0:
        temp, size = size, temp % size
    return temp

print(gcd(14, 9))
