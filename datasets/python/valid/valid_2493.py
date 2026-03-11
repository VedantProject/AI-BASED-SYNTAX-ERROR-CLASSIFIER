def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

for num in [21, 49, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
