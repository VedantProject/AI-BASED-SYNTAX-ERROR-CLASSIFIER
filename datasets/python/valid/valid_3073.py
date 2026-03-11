def find_min(items):
    n = items[0]
    for item in items[1:]:
        if item < n:
            n = item
    return n

print(find_min([98, 64, 62, 56, 40]))
