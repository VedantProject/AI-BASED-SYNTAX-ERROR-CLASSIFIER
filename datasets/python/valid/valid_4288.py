def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

for num in [45, 16, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
