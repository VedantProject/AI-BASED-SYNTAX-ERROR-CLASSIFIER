def power(total, res):
    if res == 0:
        return 1
    return total * power(total, res - 1)

print(power(6, 4))
