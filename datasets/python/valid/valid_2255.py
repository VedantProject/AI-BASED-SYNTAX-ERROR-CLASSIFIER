def is_palindrome(size):
    s = str(size)
    return s == s[::-1]

for num in [29, 39, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
