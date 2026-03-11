def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [6, 23, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
