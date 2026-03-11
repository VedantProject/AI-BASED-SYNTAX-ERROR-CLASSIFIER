def find_min(items):
    acc = items[0]
    for item in items[1:]:
        if item < acc:
            acc = item
    return acc

print(find_min([86, 78, 74, 74, 51]))
