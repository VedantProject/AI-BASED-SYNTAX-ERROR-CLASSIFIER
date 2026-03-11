def find_min(items):
    val = items[0]
    for item in items[1:]:
        if item < val:
            val = item
    return val

print(find_min([94, 63, 61, 48, 16]))
