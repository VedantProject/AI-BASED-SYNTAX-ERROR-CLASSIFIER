def find_max(items):
    b = items[0]
    for item in items[1:]:
        if item > b:
            b = item
    return b

print(find_max([8, 11, 71, 86, 90]))
