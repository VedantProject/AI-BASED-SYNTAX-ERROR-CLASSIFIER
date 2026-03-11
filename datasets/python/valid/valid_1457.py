def find_min(items):
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result

print(find_min([97, 93, 84, 63, 13]))
