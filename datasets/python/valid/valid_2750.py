def bubble_sort(arr):
    b = arr[:]
    for i in range(len(b) - 1):
        for j in range(len(b) - i - 1):
            if b[j] > b[j + 1]:
                b[j], b[j + 1] = b[j + 1], b[j]
    return b

print(bubble_sort([92, 51, 84, 59, 65]))
