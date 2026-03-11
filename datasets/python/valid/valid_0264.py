def find_min(items):
    size = items[0]
    for item in items[1:]:
        if item < size:
            size = item
    return size

print(find_min([81, 77, 57, 49, 2]))
