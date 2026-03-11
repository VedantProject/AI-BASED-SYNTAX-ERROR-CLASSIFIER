def find_max(items):
    val = items[0]
    for item in items[1:]:
        if item > val:
            val = item
    return val

print(find_max([9, 25, 39, 51, 74]))
