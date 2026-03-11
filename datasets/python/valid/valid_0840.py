def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [26, 32, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
