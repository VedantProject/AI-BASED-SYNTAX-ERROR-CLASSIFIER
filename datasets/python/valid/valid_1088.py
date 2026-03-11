def find_max(items):
    diff = items[0]
    for item in items[1:]:
        if item > diff:
            diff = item
    return diff

print(find_max([9, 19, 25, 47, 82]))
