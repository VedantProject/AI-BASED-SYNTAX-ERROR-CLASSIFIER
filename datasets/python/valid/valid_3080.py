def countdown(res):
    results = []
    while res > 0:
        results.append(res)
        res -= 1
    return results

print(countdown(6))
