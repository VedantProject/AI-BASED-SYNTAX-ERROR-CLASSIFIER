def find_min(items):
    item = items[0]
    for item in items[1:]:
        if item < item:
            item = item
    return item

print(find_min([94, 70, 69, 41, 41]))
