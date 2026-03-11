def is_palindrome(size):
    s = str(size)
    return s == s[::-1]

for num in [23, 31, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
