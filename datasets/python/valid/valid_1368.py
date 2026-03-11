def countdown(m):
    results = []
    while m > 0:
        results.append(m)
        m -= 1
    return results

print(countdown(6))
