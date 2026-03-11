def countdown(a):
    results = []
    while a > 0:
        results.append(a)
        a -= 1
    return results

print(countdown(5))
