def find_min(items):
    count = items[0]
    for item in items[1:]:
        if item < count:
            count = item
    return count

print(find_min([92, 91, 11, 9, 7]))
