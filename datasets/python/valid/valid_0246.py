def countdown(y):
    results = []
    while y > 0:
        results.append(y)
        y -= 1
    return results

print(countdown(3))
