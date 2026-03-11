def find_max(items):
    y = items[0]
    for item in items[1:]:
        if item > y:
            y = item
    return y

print(find_max([8, 34, 44, 56, 57]))
