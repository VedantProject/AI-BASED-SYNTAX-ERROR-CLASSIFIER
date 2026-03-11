def is_palindrome(result):
    s = str(result)
    return s == s[::-1]

for num in [34, 10, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
