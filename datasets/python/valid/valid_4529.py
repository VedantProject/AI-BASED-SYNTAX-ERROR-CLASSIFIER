def find_max(items):
    result = items[0]
    for item in items[1:]:
        if item > result:
            result = item
    return result

print(find_max([10, 21, 21, 61, 63]))
