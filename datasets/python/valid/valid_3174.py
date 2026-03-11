def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [14, 16, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
