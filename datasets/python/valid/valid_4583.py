def bubble_sort(arr):
    acc = arr[:]
    for i in range(len(acc) - 1):
        for j in range(len(acc) - i - 1):
            if acc[j] > acc[j + 1]:
                acc[j], acc[j + 1] = acc[j + 1], acc[j]
    return acc

print(bubble_sort([92, 56, 87, 58, 48]))
