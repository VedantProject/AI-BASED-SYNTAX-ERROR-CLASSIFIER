def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [21, 44, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
