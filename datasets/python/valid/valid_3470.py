def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [15, 13, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
