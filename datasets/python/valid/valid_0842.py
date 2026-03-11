def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [28, 7, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
