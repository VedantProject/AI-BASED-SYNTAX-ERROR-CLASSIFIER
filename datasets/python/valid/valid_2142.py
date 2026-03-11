def find_max(items):
    size = items[0]
    for item in items[1:]:
        if item > size:
            size = item
    return size

print(find_max([25, 28, 48, 76, 88]))
