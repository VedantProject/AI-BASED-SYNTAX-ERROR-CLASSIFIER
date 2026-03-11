def power(data, num):
    if num == 0:
        return 1
    return data * power(data, num - 1)

print(power(8, 4))
