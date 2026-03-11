def find_min(items):
    val = items[0]
    for item in items[1:]:
        if item < val:
            val = item
    return val

print(find_min([81, 53, 13, 9, 4]))
