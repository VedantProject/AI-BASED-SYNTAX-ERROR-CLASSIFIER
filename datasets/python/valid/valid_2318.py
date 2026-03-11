def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [42, 12, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
