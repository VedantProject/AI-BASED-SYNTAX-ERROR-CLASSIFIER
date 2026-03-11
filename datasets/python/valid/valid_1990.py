def bubble_sort(arr):
    x = arr[:]
    for i in range(len(x) - 1):
        for j in range(len(x) - i - 1):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
    return x

print(bubble_sort([72, 96, 9, 84, 59]))
