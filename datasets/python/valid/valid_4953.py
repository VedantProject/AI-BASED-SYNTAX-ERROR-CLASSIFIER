def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [16, 24, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
