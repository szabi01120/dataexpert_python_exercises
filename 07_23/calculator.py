# calculator 4 operator

class Operation:
    def __init__(self, operator):
        self.operator = operator

    def add_operator(self, x, y):
        return x + y

    def sub_operator(self, x, y):
        return x - y

    def mul_operator(self, x, y):
        return x * y

    def div_operator(self, x, y):
        return x / y

    def decide_operator(self, x, y):
        if self.operator == "+":
            return self.add_operator(x, y)
        elif self.operator == "-":
            return self.sub_operator(x, y)
        elif self.operator == "*":
            return self.mul_operator(x, y)
        elif self.operator == "/":
            return self.div_operator(x, y)
        else:
            return None

def main():
    operators = ["+", "-", "*", "/"]
    x = int(input("Add meg az első számot: "))
    y = int(input("Add meg a második számot: "))
    
    operator = input("Add meg a műveletet (+, -, *, /): ")
    operations = Operation(operator)
    
    if operator not in operators:
        print("Nem megfelelő operátor")
        return None
    
    if operator == "/" and x == 0 or y == 0:
        print("Nullával való osztást nem értelmezzük")
        return None
    
    print(operations.decide_operator(x, y))    
    
if __name__ == '__main__':
    main()