def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [45, 49, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
