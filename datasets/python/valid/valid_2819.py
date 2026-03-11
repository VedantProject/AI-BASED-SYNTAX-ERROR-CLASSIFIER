def countdown(val):
    results = []
    while val > 0:
        results.append(val)
        val -= 1
    return results

print(countdown(3))
