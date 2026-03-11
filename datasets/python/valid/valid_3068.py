def is_palindrome(data):
    s = str(data)
    return s == s[::-1]

for num in [47, 32, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
