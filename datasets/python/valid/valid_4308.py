def find_max(items):
    prod = items[0]
    for item in items[1:]:
        if item > prod:
            prod = item
    return prod

print(find_max([2, 18, 40, 58, 65]))
