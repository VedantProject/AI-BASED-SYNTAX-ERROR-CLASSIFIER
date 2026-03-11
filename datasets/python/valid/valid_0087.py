def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [22, 47, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
