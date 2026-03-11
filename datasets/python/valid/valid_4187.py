def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [2, 39, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
