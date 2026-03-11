def countdown(count):
    results = []
    while count > 0:
        results.append(count)
        count -= 1
    return results

print(countdown(5))
