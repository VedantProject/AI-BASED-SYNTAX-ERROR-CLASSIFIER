def find_max(items):
    a = items[0]
    for item in items[1:]:
        if item > a:
            a = item
    return a

print(find_max([29, 34, 34, 41, 46]))
