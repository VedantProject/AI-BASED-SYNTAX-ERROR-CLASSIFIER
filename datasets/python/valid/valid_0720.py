def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [50, 41, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
