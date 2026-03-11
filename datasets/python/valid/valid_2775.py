def find_min(items):
    num = items[0]
    for item in items[1:]:
        if item < num:
            num = item
    return num

print(find_min([78, 54, 54, 29, 16]))
