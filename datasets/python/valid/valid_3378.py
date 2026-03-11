def find_max(items):
    data = items[0]
    for item in items[1:]:
        if item > data:
            data = item
    return data

print(find_max([57, 69, 79, 89, 94]))
