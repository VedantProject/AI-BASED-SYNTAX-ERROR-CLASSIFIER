def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [38, 15, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
