'''

Symbolic Differentation in Python from Scratch!

'''

is_variable = lambda x: isinstance(x, str) and x in "abcdefghijklmnopqrstuvwxyz"

def parse_variable(text):
    """
    Checks if text is a single lowercase english letter, and returns it if so.

    >>> parse_variable('x')
    'x'
    >>> parse_variable('y')
    'y'
    >>> parse_variable('1')
    >>> parse_variable('x + 4')
    """
    if is_variable(text):
        return text

def parse_number(text):
    """
    >>> parse_number('1')
    1
    >>> parse_number('-2.5')
    -2.5
    >>> parse_number('.0')
    0.0
    >>> parse_number('x + 4')
    """
    def char_is_number(char):
        return char in "1234567890"

    negative = False
    if "-" == text[0]:
        negative = True
        text = text[1:]

    if all(map(char_is_number, text)):
        if negative:
            return -1 * int(text)
        return int(text)

    text_no_period = text.replace(".", "", 1)
    if all(map(char_is_number, text_no_period)):
        if negative:
            return -1 * float(text)
        return float(text)

def parse_binary_operator(text, operator, operator_name):
    if text.count(operator) >= 1:
        split = text.split(operator, 1)
        left, right = parse(split[0]), parse(split[1])
        if left != None and right != None:
            return [operator_name, left, right]
    

def parse_plus(text):
    """
    >>> parse_plus('x+4')
    ['plus', 'x', 4]
    >>> parse_plus('x + 4')
    ['plus', 'x', 4]
    >>> parse_plus('x + y + z')
    ['plus', 'x', ['plus', 'y', 'z']]
    >>> parse_plus('x + + 2')
    """
    return parse_binary_operator(text, '+', 'plus')

def parse_mul(text):
    """
    >>> parse_mul('x*4')
    ['mul', 'x', 4]
    """
    return parse_binary_operator(text, '*', 'mul')

def parse_pow(text):
    """
    >>> parse_pow('x^3')
    ['pow', 'x', 3]
    """
    return parse_binary_operator(text, '^', 'pow')

def parse(text):
    """
    Parses an input formula to derive.

    >>> parse('x + 4')
    ['plus', 'x', 4]
    >>> parse('x')
    'x'
    >>> parse('5.6')
    5.6
    >>> parse('y + x + z')
    ['plus', 'y', ['plus', 'x', 'z']]
    >>> parse('4*x + -2*z')
    ['plus', ['mul', 4, 'x'], ['mul', -2, 'z']]
    >>> parse('3*x^4')
    ['mul', 3, ['pow', 'x', 4]]
    """
    text = text.replace(" ", "")
    if text == "":
        return None
    if (x := parse_variable(text)) != None:
        return x
    if (x := parse_number(text)) != None:
        return x
    if (x := parse_plus(text)) != None:
        return x
    if (x := parse_mul(text)) != None:
        return x
    if (x := parse_pow(text)) != None:
        return x

is_int = lambda x: isinstance(x, int)
is_float = lambda x: isinstance(x, float)

def plus(left, right):
    """
    >>> plus('x', 'y')
    ['plus', 'x', 'y']
    >>> plus('x', 0)
    'x'
    >>> plus(1.0, -2.0)
    -1.0
    """
    if left == 0 or left == 0.0:
        return right
    if right == 0 or right == 0.0:
        return left
    if (is_int(left) or is_float(left)) and (is_int(right) or is_float(right)):
        return left + right
    return ['plus', left, right]

def mul(left, right):
    """
    >>> mul(0, "x")
    0
    >>> mul('y', 1.0)
    'y'
    >>> mul(4, 2.5)
    10.0
    >>> mul('x', 2)
    ['mul', 'x', 2]
    """
    if left == 0 or left == 0.0 or right == 0 or right == 0.0:
        return 0
    if left == 1 or left == 1.0:
        return right
    if right == 1 or right == 1.0:
        return left
    if (is_int(left) or is_float(left)) and (is_int(right) or is_float(right)):
        return left * right
    return ['mul', left, right]

def sub(left, right):
    """
    >>> sub('x', 0)
    'x'
    >>> sub(1.5, .5)
    1.0
    >>> sub(0, 'x')
    ['sub', 0, 'x']
    """
    if right == 0 or right == 0.0:
        return left
    if (is_int(left) or is_float(left)) and (is_int(right) or is_float(right)):
        return left - right
    return ['sub', left, right]

def pow(left, right):
    """
    >>> pow('x', 0)
    1
    >>> pow('y', 1)
    'y'
    >>> pow(0, 'x')
    0
    """
    if right == 0 or right == 0.0:
        return 1
    if right == 1 or right == 1.0:
        return left
    if left == 0 or left == 0.0:
        return 0
    return ['pow', left, right]
    
    
    
def derive(expr):
    """
    Derivation of `expr` with respect to `x`
    d(expr)
    -------
      dx

    >>> derive(5.6)
    0
    >>> derive('x')
    1
    >>> derive('y')
    0
    >>> derive(parse('x + y'))
    1
    >>> derive(parse('4*x + 3*y'))
    4
    """
    if is_int(expr) or is_float(expr):
        return 0
    if is_variable(expr):
        if expr == 'x':
            return 1
        else:
            return 0
    operator, left, right = expr
    if operator == 'plus':
        return plus(derive(left), derive(right))
    if operator == 'mul':
        return plus(mul(left, derive(right)), mul(right, derive(left)))
    if operator == 'pow':
        # d(u^n)                du
        # ----- = n*(u^(n-1))* ----
        #  dx                   dx
        return mul(mul(right, pow(left, sub(right, 1))), derive(left))

def evaluate(expr):
    """
    Turn an expression back into a human readable string
    
    >>> evaluate("x")
    'x'
    >>> evaluate(["plus", 'x', 'y'])
    'x + y'
    >>> evaluate(["mul", 'x', 'y'])
    'x*y'
    """
    if is_int(expr) or is_float(expr):
        return str(expr)
    if is_variable(expr):
        return expr
    
    operator, left, right = expr
    if operator == "plus":
        return f"{evaluate(left)} + {evaluate(right)}"
    if operator == "sub":
        return f"{evaluate(left)} - {evaluate(right)}"
    if operator == "mul":
        return f"{evaluate(left)}*{evaluate(right)}"
    if operator == "pow":
        return f"{evaluate(left)}^{evaluate(right)}"
    
def apdepr():
    # ask
    x = input("> ")
    # parse
    parsed = parse(x)
    # derive
    derived = derive(parsed)
    # evaluate
    evaluated = evaluate(derived)
    # print
    print(evaluated)
    # recurse
    apdepr()

if __name__ == "__main__":
    apdepr()
