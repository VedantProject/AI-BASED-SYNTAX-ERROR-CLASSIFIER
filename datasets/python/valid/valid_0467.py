class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        self.result = x + y
        return self.result
    
    def get_result(self):
        return self.result

if __name__ == "__main__":
    calc = Calculator()
    calc.add(5, 10)
    print(f"Result: {calc.get_result()}")
