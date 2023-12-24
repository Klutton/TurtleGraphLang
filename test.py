import turtle
import math

# 词法分析器
def lexer(expression):
    # 将表达式拆分为词语
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    return tokens

# 语法分析器
def parse(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected end of input")

    token = tokens.pop(0)

    if token == '(':
        # 开始解析子表达式
        expression = []
        while tokens[0] != ')':
            expression.append(parse(tokens))
        tokens.pop(0)  # 弹出 ')'
        return expression
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        # 数字或函数名
        try:
            return float(token)
        except ValueError:
            return token

# 计算表达式的值
def evaluate(expression, x):
    if isinstance(expression, list):
        # 如果是子表达式，递归计算每个元素的值
        if expression[0] == 'sin':
            return math.sin(evaluate(expression[1], x))
        elif expression[0] == 'cos':
            return math.cos(evaluate(expression[1], x))
        elif expression[0] == 'tan':
            return math.tan(evaluate(expression[1], x))
        elif expression[0] == 'sqrt':
            return math.sqrt(evaluate(expression[1], x))
        elif expression[0] == '+':
            return evaluate(expression[1], x) + evaluate(expression[2], x)
        elif expression[0] == '-':
            return evaluate(expression[1], x) - evaluate(expression[2], x)
        elif expression[0] == '*':
            return evaluate(expression[1], x) * evaluate(expression[2], x)
        elif expression[0] == '/':
            return evaluate(expression[1], x) / evaluate(expression[2], x)
    else:
        # 数字或变量
        if expression == 'x':
            return x
        else:
            return expression

# 绘图函数
def draw_function(expression, x_range=(-10, 10), step=0.1):
    turtle.speed(2)
    turtle.penup()

    for x in range(int(x_range[0] / step), int(x_range[1] / step)):
        turtle.goto(x * step, evaluate(expression, x * step))
        turtle.pendown()

    turtle.done()

# 示例用法
expression = '(+ (* 2 x) (* 3 (sin x)))'
tokens = lexer(expression)
parsed_expression = parse(tokens)

draw_function(parsed_expression, x_range=(-10, 10), step=0.1)
