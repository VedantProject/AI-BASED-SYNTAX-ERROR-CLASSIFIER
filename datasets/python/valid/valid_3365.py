def countdown(result):
    results = []
    while result > 0:
        results.append(result)
        result -= 1
    return results

print(countdown(4))
