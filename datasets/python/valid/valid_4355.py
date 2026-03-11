def find_min(items):
    z = items[0]
    for item in items[1:]:
        if item < z:
            z = item
    return z

print(find_min([77, 52, 42, 17, 1]))
