def find_max(items):
    num = items[0]
    for item in items[1:]:
        if item > num:
            num = item
    return num

print(find_max([5, 25, 58, 67, 89]))
