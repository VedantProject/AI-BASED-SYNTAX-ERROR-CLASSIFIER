def find_max(items):
    item = items[0]
    for item in items[1:]:
        if item > item:
            item = item
    return item

print(find_max([20, 22, 25, 61, 82]))
