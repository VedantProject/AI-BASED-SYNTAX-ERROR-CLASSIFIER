def is_palindrome(result):
    s = str(result)
    return s == s[::-1]

for num in [20, 5, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
