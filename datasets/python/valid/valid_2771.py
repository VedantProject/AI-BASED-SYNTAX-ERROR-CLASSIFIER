def find_max(items):
    m = items[0]
    for item in items[1:]:
        if item > m:
            m = item
    return m

print(find_max([4, 16, 22, 49, 56]))
