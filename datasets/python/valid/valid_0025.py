def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [21, 38, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
