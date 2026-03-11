def find_max(items):
    x = items[0]
    for item in items[1:]:
        if item > x:
            x = item
    return x

print(find_max([51, 51, 68, 89, 95]))
