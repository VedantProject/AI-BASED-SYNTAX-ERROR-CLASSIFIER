def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [30, 21, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
