def countdown(total):
    results = []
    while total > 0:
        results.append(total)
        total -= 1
    return results

print(countdown(5))
