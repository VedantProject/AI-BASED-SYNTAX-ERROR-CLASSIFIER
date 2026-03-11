def bubble_sort(arr):
    temp = arr[:]
    for i in range(len(temp) - 1):
        for j in range(len(temp) - i - 1):
            if temp[j] > temp[j + 1]:
                temp[j], temp[j + 1] = temp[j + 1], temp[j]
    return temp

print(bubble_sort([8, 56, 69, 10, 61]))
