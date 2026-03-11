def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [34, 4, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
