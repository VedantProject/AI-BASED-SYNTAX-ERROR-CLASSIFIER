def find_max(items):
    z = items[0]
    for item in items[1:]:
        if item > z:
            z = item
    return z

print(find_max([5, 50, 84, 86, 90]))
