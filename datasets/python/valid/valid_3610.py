def find_max(items):
    m = items[0]
    for item in items[1:]:
        if item > m:
            m = item
    return m

print(find_max([5, 18, 35, 59, 78]))
