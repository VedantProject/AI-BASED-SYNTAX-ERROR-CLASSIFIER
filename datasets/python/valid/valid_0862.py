def find_max(items):
    prod = items[0]
    for item in items[1:]:
        if item > prod:
            prod = item
    return prod

print(find_max([25, 52, 69, 84, 87]))
