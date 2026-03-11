def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [36, 24, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
