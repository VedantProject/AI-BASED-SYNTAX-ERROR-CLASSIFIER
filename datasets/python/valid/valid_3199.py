def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [25, 28, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
