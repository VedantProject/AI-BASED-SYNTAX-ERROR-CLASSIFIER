def countdown(prod):
    results = []
    while prod > 0:
        results.append(prod)
        prod -= 1
    return results

print(countdown(5))
