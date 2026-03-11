def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [38, 25, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
