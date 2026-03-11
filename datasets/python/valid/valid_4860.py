def countdown(temp):
    results = []
    while temp > 0:
        results.append(temp)
        temp -= 1
    return results

print(countdown(2))
