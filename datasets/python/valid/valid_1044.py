def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [37, 15, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
