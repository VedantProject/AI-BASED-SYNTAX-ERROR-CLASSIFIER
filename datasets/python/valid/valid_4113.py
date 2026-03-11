def find_max(items):
    y = items[0]
    for item in items[1:]:
        if item > y:
            y = item
    return y

print(find_max([5, 20, 54, 68, 95]))
