def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen(21, 35, 3)))
