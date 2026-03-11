def bubble_sort(arr):
    num = arr[:]
    for i in range(len(num) - 1):
        for j in range(len(num) - i - 1):
            if num[j] > num[j + 1]:
                num[j], num[j + 1] = num[j + 1], num[j]
    return num

print(bubble_sort([74, 27, 29, 41, 45]))
