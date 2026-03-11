def gcd(item, data):
    while data != 0:
        item, data = data, item % data
    return item

print(gcd(20, 29))
