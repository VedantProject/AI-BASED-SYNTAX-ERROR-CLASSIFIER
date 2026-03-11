def is_palindrome(z):
    s = str(z)
    return s == s[::-1]

for num in [43, 15, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
