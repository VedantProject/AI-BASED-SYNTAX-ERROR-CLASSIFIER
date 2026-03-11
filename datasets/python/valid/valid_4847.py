def find_min(items):
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result

print(find_min([49, 45, 44, 26, 15]))
