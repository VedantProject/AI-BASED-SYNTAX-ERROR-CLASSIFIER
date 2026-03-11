def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [33, 29, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
