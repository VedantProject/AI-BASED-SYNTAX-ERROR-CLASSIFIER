def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [22, 6, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
