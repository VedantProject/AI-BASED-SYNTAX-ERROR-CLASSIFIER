def find_min(items):
    data = items[0]
    for item in items[1:]:
        if item < data:
            data = item
    return data

print(find_min([96, 80, 49, 45, 15]))
