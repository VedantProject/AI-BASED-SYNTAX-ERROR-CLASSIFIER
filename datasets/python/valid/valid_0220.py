def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [32, 12, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
