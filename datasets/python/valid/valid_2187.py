def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [5, 12, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
