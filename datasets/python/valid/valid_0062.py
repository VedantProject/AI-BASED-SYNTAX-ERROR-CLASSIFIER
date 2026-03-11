def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [34, 13, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
