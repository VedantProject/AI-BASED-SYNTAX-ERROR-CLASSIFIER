def is_palindrome(count):
    s = str(count)
    return s == s[::-1]

for num in [48, 34, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
