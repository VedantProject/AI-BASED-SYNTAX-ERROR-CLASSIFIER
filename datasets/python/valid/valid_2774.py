def find_min(items):
    prod = items[0]
    for item in items[1:]:
        if item < prod:
            prod = item
    return prod

print(find_min([97, 54, 51, 14, 12]))
