def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [21, 40, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
