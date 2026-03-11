def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [6, 46, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
