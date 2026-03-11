def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [40, 46, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
