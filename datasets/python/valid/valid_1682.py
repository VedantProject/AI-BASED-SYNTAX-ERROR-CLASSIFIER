def find_min(items):
    data = items[0]
    for item in items[1:]:
        if item < data:
            data = item
    return data

print(find_min([95, 89, 67, 62, 30]))
