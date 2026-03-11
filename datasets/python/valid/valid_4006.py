def countdown(acc):
    results = []
    while acc > 0:
        results.append(acc)
        acc -= 1
    return results

print(countdown(9))
