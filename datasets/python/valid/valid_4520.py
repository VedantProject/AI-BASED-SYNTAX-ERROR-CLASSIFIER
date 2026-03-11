def is_palindrome(y):
    s = str(y)
    return s == s[::-1]

for num in [2, 31, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
