def find_max(items):
    total = items[0]
    for item in items[1:]:
        if item > total:
            total = item
    return total

print(find_max([18, 20, 31, 36, 74]))
