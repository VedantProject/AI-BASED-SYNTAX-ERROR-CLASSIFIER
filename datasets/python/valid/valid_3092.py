def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [49, 46, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
