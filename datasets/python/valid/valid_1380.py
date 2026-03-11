def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [15, 18, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
