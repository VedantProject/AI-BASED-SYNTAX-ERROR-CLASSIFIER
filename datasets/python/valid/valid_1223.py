def countdown(num):
    results = []
    while num > 0:
        results.append(num)
        num -= 1
    return results

print(countdown(9))
