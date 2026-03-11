def find_max(items):
    m = items[0]
    for item in items[1:]:
        if item > m:
            m = item
    return m

print(find_max([26, 34, 45, 56, 89]))
