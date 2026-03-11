def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [36, 15, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
