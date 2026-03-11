def is_palindrome(m):
    s = str(m)
    return s == s[::-1]

for num in [20, 50, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
