def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [13, 19, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
