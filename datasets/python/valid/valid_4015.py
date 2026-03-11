def bubble_sort(arr):
    size = arr[:]
    for i in range(len(size) - 1):
        for j in range(len(size) - i - 1):
            if size[j] > size[j + 1]:
                size[j], size[j + 1] = size[j + 1], size[j]
    return size

print(bubble_sort([91, 27, 22, 21, 78]))
