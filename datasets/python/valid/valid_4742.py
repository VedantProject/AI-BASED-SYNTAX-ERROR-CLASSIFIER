def bubble_sort(arr):
    y = arr[:]
    for i in range(len(y) - 1):
        for j in range(len(y) - i - 1):
            if y[j] > y[j + 1]:
                y[j], y[j + 1] = y[j + 1], y[j]
    return y

print(bubble_sort([44, 69, 96, 71, 87]))
