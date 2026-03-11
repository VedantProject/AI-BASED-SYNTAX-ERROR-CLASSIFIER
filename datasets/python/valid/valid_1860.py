def countdown(size):
    results = []
    while size > 0:
        results.append(size)
        size -= 1
    return results

print(countdown(3))
