def find_max(items):
    count = items[0]
    for item in items[1:]:
        if item > count:
            count = item
    return count

print(find_max([23, 46, 63, 81, 96]))
