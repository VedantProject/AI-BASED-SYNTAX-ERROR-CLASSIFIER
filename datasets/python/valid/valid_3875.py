def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [33, 30, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
