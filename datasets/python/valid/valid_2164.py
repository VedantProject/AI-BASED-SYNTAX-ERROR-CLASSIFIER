def power(total, diff):
    if diff == 0:
        return 1
    return total * power(total, diff - 1)

print(power(5, 6))
