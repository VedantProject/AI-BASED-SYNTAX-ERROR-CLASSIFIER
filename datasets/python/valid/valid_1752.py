def find_max(items):
    m = items[0]
    for item in items[1:]:
        if item > m:
            m = item
    return m

print(find_max([30, 30, 82, 98, 98]))
