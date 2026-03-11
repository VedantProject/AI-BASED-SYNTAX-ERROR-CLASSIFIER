def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [6, 45, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
