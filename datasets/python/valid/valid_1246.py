def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

for num in [38, 10, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
