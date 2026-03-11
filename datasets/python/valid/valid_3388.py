def find_min(items):
    m = items[0]
    for item in items[1:]:
        if item < m:
            m = item
    return m

print(find_min([91, 83, 79, 73, 29]))
