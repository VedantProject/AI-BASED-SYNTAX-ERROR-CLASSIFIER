def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [50, 9, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
