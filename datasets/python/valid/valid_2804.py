def find_max(items):
    total = items[0]
    for item in items[1:]:
        if item > total:
            total = item
    return total

print(find_max([2, 18, 48, 74]))
