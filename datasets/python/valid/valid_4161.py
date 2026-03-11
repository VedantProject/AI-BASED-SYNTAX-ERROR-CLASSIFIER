def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [7, 33, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
