def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [37, 49, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
