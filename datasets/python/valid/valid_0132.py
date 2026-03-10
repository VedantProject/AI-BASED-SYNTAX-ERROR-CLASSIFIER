def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    print(f"Sum: {sum_list(nums)}")
