def is_palindrome(size):
    s = str(size)
    return s == s[::-1]

for num in [40, 8, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
