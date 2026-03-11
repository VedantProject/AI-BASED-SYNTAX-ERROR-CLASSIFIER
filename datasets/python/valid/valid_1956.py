def bubble_sort(arr):
    data = arr[:]
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

print(bubble_sort([75, 26, 13, 31, 70]))
