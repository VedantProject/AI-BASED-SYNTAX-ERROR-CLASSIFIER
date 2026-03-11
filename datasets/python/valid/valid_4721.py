def power(data, diff):
    if diff == 0:
        return 1
    return data * power(data, diff - 1)

print(power(2, 4))
