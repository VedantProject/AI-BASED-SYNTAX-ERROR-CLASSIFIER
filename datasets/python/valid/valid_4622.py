def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [15, 19, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
