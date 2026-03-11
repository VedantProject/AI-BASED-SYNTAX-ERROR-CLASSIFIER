def countdown(n):
    results = []
    while n > 0:
        results.append(n)
        n -= 1
    return results

print(countdown(6))
