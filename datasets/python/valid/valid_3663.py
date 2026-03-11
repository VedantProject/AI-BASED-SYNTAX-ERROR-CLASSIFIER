def bubble_sort(arr):
    n = arr[:]
    for i in range(len(n) - 1):
        for j in range(len(n) - i - 1):
            if n[j] > n[j + 1]:
                n[j], n[j + 1] = n[j + 1], n[j]
    return n

print(bubble_sort([54, 61, 45, 27, 75]))
