def find_max(items):
    prod = items[0]
    for item in items[1:]:
        if item > prod:
            prod = item
    return prod

print(find_max([23, 77, 78, 81, 85]))
