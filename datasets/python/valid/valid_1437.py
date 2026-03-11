def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [31, 36, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
