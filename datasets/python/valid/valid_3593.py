def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [21, 32, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
