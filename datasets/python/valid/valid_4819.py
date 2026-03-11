def bubble_sort(arr):
    data = arr[:]
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

print(bubble_sort([69, 59, 42, 89, 70]))
