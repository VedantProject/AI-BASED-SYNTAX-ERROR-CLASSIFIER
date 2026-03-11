def find_min(items):
    diff = items[0]
    for item in items[1:]:
        if item < diff:
            diff = item
    return diff

print(find_min([87, 69, 49, 46, 7]))
