def is_palindrome(temp):
    s = str(temp)
    return s == s[::-1]

for num in [22, 45, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
