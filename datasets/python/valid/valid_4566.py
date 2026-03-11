def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [44, 12, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
