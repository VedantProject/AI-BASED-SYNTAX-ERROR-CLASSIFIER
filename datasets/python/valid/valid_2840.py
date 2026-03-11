def countdown(data):
    results = []
    while data > 0:
        results.append(data)
        data -= 1
    return results

print(countdown(4))
