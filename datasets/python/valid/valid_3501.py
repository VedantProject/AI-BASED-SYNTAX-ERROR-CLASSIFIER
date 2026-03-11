def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [18, 16, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
