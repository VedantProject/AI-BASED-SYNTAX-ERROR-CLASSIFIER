def is_palindrome(count):
    s = str(count)
    return s == s[::-1]

for num in [50, 33, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
