def find_max(items):
    x = items[0]
    for item in items[1:]:
        if item > x:
            x = item
    return x

print(find_max([13, 16, 56, 69, 88]))
