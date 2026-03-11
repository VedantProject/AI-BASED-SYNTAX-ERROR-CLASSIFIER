def find_max(items):
    num = items[0]
    for item in items[1:]:
        if item > num:
            num = item
    return num

print(find_max([13, 15, 19, 33, 91]))
