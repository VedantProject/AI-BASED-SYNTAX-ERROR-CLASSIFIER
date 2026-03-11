def find_min(items):
    diff = items[0]
    for item in items[1:]:
        if item < diff:
            diff = item
    return diff

print(find_min([92, 52, 47, 43, 19]))
