def countdown(x):
    results = []
    while x > 0:
        results.append(x)
        x -= 1
    return results

print(countdown(5))
