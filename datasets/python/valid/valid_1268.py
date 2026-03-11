def countdown(z):
    results = []
    while z > 0:
        results.append(z)
        z -= 1
    return results

print(countdown(8))
