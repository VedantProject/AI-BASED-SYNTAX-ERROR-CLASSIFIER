def is_palindrome(data):
    s = str(data)
    return s == s[::-1]

for num in [44, 8, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
