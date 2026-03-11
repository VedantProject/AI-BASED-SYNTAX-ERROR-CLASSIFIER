def is_palindrome(count):
    s = str(count)
    return s == s[::-1]

for num in [32, 5, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
