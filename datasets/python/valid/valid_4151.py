def is_palindrome(data):
    s = str(data)
    return s == s[::-1]

for num in [10, 23, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
