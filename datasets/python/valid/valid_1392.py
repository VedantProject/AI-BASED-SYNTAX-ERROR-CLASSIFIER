def power(count, num):
    if num == 0:
        return 1
    return count * power(count, num - 1)

print(power(10, 5))
