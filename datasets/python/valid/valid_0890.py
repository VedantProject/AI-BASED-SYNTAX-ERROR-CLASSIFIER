def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [33, 5, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
