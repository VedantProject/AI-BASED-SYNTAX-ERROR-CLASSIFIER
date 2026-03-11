def find_min(items):
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result

print(find_min([90, 82, 82, 72, 59]))
