def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [10, 28, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
