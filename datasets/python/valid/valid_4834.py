def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [25, 6, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
