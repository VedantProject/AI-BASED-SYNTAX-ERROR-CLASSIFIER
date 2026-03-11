def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [47, 10, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
