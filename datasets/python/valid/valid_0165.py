def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [32, 5, 121, 131, 5]:
    print(f"{num}: {is_palindrome(num)}")
