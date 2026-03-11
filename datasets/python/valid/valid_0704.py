def find_min(items):
    size = items[0]
    for item in items[1:]:
        if item < size:
            size = item
    return size

print(find_min([93, 90, 85, 25, 16]))
