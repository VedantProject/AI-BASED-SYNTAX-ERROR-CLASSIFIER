def power(data, count):
    if count == 0:
        return 1
    return data * power(data, count - 1)

print(power(10, 5))
