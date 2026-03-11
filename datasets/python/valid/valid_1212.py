def gcd(total, size):
    while size != 0:
        total, size = size, total % size
    return total

print(gcd(54, 40))
