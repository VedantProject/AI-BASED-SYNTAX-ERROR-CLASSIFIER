def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

for num in [10, 35, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
