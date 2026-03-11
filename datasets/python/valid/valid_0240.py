def is_palindrome(size):
    s = str(size)
    return s == s[::-1]

for num in [25, 9, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
