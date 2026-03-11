def countdown(diff):
    results = []
    while diff > 0:
        results.append(diff)
        diff -= 1
    return results

print(countdown(9))
