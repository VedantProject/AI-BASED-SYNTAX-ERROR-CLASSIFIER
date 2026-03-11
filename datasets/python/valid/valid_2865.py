def is_palindrome(size):
    s = str(size)
    return s == s[::-1]

for num in [50, 50, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
