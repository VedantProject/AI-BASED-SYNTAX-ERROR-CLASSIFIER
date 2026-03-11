def find_min(items):
    total = items[0]
    for item in items[1:]:
        if item < total:
            total = item
    return total

print(find_min([94, 87, 18, 10, 6]))
