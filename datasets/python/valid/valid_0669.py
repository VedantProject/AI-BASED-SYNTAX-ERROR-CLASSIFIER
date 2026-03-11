def find_max(items):
    total = items[0]
    for item in items[1:]:
        if item > total:
            total = item
    return total

print(find_max([24, 42, 49, 66, 68]))
