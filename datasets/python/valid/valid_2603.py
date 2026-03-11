def power(total, count):
    if count == 0:
        return 1
    return total * power(total, count - 1)

print(power(11, 5))
