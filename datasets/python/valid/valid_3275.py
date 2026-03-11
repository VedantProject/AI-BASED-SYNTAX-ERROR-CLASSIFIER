def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [7, 29, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
