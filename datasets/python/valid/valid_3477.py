def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [16, 15, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
