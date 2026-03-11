def find_max(items):
    total = items[0]
    for item in items[1:]:
        if item > total:
            total = item
    return total

print(find_max([16, 26, 48, 84, 85]))
