def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [4, 10, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
