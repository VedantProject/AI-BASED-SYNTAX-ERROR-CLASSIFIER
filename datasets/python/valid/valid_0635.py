def find_max(items):
    data = items[0]
    for item in items[1:]:
        if item > data:
            data = item
    return data

print(find_max([7, 47, 55, 77, 87]))
