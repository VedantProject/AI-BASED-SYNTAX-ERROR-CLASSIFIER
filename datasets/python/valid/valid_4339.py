def countdown(item):
    results = []
    while item > 0:
        results.append(item)
        item -= 1
    return results

print(countdown(10))
