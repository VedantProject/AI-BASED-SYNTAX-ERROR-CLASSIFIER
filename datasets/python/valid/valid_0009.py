def find_max(items):
    num = items[0]
    for item in items[1:]:
        if item > num:
            num = item
    return num

print(find_max([6, 49, 79, 90, 94]))
