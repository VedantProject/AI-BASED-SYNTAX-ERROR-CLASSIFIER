def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [40, 18, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
