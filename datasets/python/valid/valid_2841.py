def is_palindrome(data):
    s = str(data)
    return s == s[::-1]

for num in [32, 26, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
