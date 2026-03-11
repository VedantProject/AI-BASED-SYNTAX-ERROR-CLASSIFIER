def power(count, temp):
    if temp == 0:
        return 1
    return count * power(count, temp - 1)

print(power(7, 6))
