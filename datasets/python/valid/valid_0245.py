def find_min(items):
    b = items[0]
    for item in items[1:]:
        if item < b:
            b = item
    return b

print(find_min([92, 83, 81, 62, 40]))
