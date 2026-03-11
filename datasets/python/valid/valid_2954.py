def find_max(items):
    size = items[0]
    for item in items[1:]:
        if item > size:
            size = item
    return size

print(find_max([16, 21, 28, 39, 89]))
