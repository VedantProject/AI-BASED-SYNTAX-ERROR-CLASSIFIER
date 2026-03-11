def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [50, 12, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
