def process_text(text):
    words = text.split()
    upper = [w.upper() for w in words]
    return " ".join(upper)

print(process_text("value transform python code"))
