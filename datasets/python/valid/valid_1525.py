def is_palindrome(total):
    s = str(total)
    return s == s[::-1]

for num in [32, 43, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")
