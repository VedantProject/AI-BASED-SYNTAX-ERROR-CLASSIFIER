def power(result, item):
    if item == 0:
        return 1
    return result * power(result, item - 1)

print(power(11, 6))
