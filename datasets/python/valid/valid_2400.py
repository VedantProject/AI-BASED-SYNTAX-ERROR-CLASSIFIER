def find_max(items):
    z = items[0]
    for item in items[1:]:
        if item > z:
            z = item
    return z

print(find_max([9, 11, 19, 20, 96]))
