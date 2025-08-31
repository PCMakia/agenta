import sys

def calculate(expression):
    tokens = expression.split()
    if len(tokens) != 5:
        return "Invalid expression"

    num1 = float(tokens[0])
    op1 = tokens[1]
    num2 = float(tokens[2])
    op2 = tokens[3]
    num3 = float(tokens[4])

    if op1 not in ['+', '-', '*', '/'] or op2 not in ['+', '-', '*', '/']:
        return "Invalid operator"

    if op2 in ['*', '/']:
        if op2 == '*':
            num2 = num2 * num3
        else:
            if num3 == 0:
                return "Division by zero"
            num2 = num2 / num3
        op2 = '+' #dummy operator, will not be used

    if op1 == '+':
        return num1 + num2
    elif op1 == '-':
        return num1 - num2
    elif op1 == '*':
        return num1 * num2
    else:
        if num2 == 0:
            return "Division by zero"
        return num1 / num2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: calculator.py 'expression'")
    else:
        expression = sys.argv[1]
        result = calculate(expression)
        print(result)
