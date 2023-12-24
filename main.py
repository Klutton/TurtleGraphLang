import turtle
import math


# 词法分析器
def lexer(expression):
    # 将表达式拆分为词语
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    return tokens


# 检查内容合法性
def valid_char(char:str):
    if char.isnumeric():
        return float(char)
    elif char in ['+', '-', '*', '/', '^', 'sin', 'cos', 'tan', 'sqrt', 'x']:
        return char
    else:
        raise SyntaxError("Unexpected character: {}".format(char))


# 语法分析器
def parse_infix(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected end of input")

    token = tokens.pop(0)

    if token == '(':
        # 开始解析子表达式
        expression = []
        while tokens[0] != ')':
            expression.append(parse_infix(tokens))
        tokens.pop(0)  # 弹出 ')'
        return expression
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        # 对字符进行检查和返回
        return valid_char(token)


# 将中缀表达式转换为后缀表达式
def infix_to_postfix(infix_expression):
    operator_stack = []
    postfix_expression = []

    # 运算符优先级
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'sin': 3, 'cos': 3, 'tan': 3, 'sqrt': 3, '^': 4}

    for token in infix_expression:
        if isinstance(token, float):
            postfix_expression.append(token)
        elif isinstance(token, list):
            postfix_expression.extend(infix_to_postfix(token))
        elif token in precedence:
            while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence[token]:
                postfix_expression.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix_expression.append(operator_stack.pop())
            operator_stack.pop()  # 弹出 '('
        elif token == 'x':
            postfix_expression.append(token)
        else:
            raise SyntaxError("Unexpected character: {}".format(token))

    while operator_stack:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression


# 计算后缀表达式的值
def evaluate_postfix(postfix_expression, x):
    stack = []

    for token in postfix_expression:
        if isinstance(token, float):
            stack.append(token)
        elif token == 'x':
            stack.append(x)
        elif token in {'+', '-', '*', '/', '^'}:
            if len(stack) < 2:
                raise SyntaxError("Not enough operands for operator {}".format(token))
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == '+':
                stack.append(operand1 + operand2)
            elif token == '-':
                stack.append(operand1 - operand2)
            elif token == '*':
                stack.append(operand1 * operand2)
            elif token == '/':
                if operand2 == 0:
                    raise ValueError("Division by zero")
                stack.append(operand1 / operand2)
            elif token == '^':
                stack.append(operand1 ** operand2)
        elif token in {'sin', 'cos', 'tan', 'sqrt'}:
            if len(stack) < 1:
                raise SyntaxError("Not enough operands for operator {}".format(token))
            operand = stack.pop()
            if token == 'sin':
                stack.append(math.sin(operand))
            elif token == 'cos':
                stack.append(math.cos(operand))
            elif token == 'tan':
                stack.append(math.tan(operand))
            elif token == 'sqrt':
                if operand < 0:
                    raise ValueError("Square root of a negative number")
                stack.append(math.sqrt(operand))

    if len(stack) != 1:
        raise SyntaxError("Invalid expression")

    return stack[0]


# 绘图函数
def draw_function_infix(infix_expression, x_range=(-10, 10), step=0.1, zoom=1.0):
    turtle.hideturtle()
    turtle.speed(100)
    turtle.penup()

    postfix_expression = infix_to_postfix(infix_expression)

    size = zoom/step

    for x in range(int(x_range[0] / step), int(x_range[1] / step)):
        turtle.goto(x * step * size, evaluate_postfix(postfix_expression, x * step) * size)
        turtle.pendown()

    turtle.done()


# 示例用法
infix_expression = '(2 * sqrt(x ^ 2) + 3 * sin(x))'
tokens = lexer(infix_expression)
parsed_expression = parse_infix(tokens)

draw_function_infix(parsed_expression, x_range=(-10, 10), step=0.1, zoom=1.2)
