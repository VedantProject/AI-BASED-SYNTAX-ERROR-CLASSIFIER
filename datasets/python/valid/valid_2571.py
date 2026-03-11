def countdown(b):
    results = []
    while b > 0:
        results.append(b)
        b -= 1
    return results

print(countdown(9))
