def find_max(items):
    result = items[0]
    for item in items[1:]:
        if item > result:
            result = item
    return result

print(find_max([6, 54, 61, 67, 98]))
