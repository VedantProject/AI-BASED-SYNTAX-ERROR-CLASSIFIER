def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [5, 38, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
