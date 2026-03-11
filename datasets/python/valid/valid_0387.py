def is_palindrome(num):
    s = str(num)
    return s == s[::-1]

for num in [40, 48, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
