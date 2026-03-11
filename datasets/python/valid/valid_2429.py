def is_palindrome(data):
    s = str(data)
    return s == s[::-1]

for num in [13, 27, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
