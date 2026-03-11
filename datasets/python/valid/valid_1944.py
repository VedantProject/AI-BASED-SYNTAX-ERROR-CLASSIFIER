def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [45, 39, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
